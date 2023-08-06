#!/usr/bin/python3
"""
    Web Source Discovery Tool

    Copyright (c) 2021 HACKER Consulting s.r.o.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

__version__ = "0.0.5"

import argparse
import datetime
import time
import itertools
import os
import sys
import urllib
import re
import requests
import tldextract
import copy
import ptlibs.ptjsonlib as ptjsonlib
import ptlibs.ptmisclib as ptmisclib
from ptthreads import ptthreads
from ptwebdiscover.utils import treeshow

class ptwebdiscover():
    def __init__(self, args):
        self.args                   = args
        self.args.timeout           = args.timeout / 1000
        self.args.delay             = args.delay / 1000
        self.args.is_star           = True if "*" in args.url else False
        self.args.nochanged_url     = self.args.url
        self.args.url               = ptmisclib.remove_slash_from_end_url(args.url) if not self.args.is_star else args.url
        self.args.url               = self.add_missing_scheme(args.url)
        self.args.target            = self.add_missing_scheme(args.target)
        self.args.position, self.args.url = self.get_star_position(self.args.url)
        self.args.headers           = ptmisclib.get_request_headers(args)
        self.args.proxies           = {"http": args.proxy, "https": args.proxy}
        self.args.charset           = ptmisclib.get_charset(["lowercase"]) if not args.charsets and not args.wordlist else ptmisclib.get_charset(args.charsets)
        self.args.parse             = args.parse or args.parse_only
        self.args.begin_with        = args.begin_with if args.begin_with else ""
        self.args.length_max        = args.length_max if args.length_max else 99 if args.wordlist else 6 
        self.args.threads           = args.threads    if not args.delay  else 1
        self.args.method            = args.method     if not (args.string_in_response or args.string_not_in_response or args.parse or args.save) else "GET"
        self.domain                 = self.get_domain_from_url(self.args.url, level=True, with_protocol=False)
        self.domain_with_protocol   = self.get_domain_from_url(self.args.url, level=True, with_protocol=True)
        self.domain_protocol        = urllib.parse.urlparse(args.url).scheme
        self.args.is_star_in_domain = True if self.args.is_star and self.args.position < len(self.domain_with_protocol)+1 else False
        self.urlpath                = self.get_path_from_url(self.args.url, with_l_slash=True, without_r_slash=True)
        self.args.auth              = tuple(args.auth.split(":")) if args.auth else None
        self.ptjsonlib              = ptjsonlib.ptjsonlib(self.args.json)
        self.ptthreads              = ptthreads.ptthreads()
        self.printlock              = ptthreads.printlock()
        self.arraylock              = ptthreads.arraylock()
        self.json_no                = self.ptjsonlib.add_json("ptwebdiscover")
        self.findings               = []
        self.findings2              = []
        self.findings_details       = []
        self.visited                = []
        self.technologies           = []
        self.directories            = [self.urlpath + "/"] if not self.args.is_star else [""]
        self.check_args_combinations()
        self.args.extensions        = self.prepare_extensions(args) # must be placed after set of self.directories
        self.prepare_not_directories(self.args.not_directories)
        
    def run(self, args):
        if not args.without_dns_cache:
            from ptwebdiscover.utils import cachefile
        ptmisclib.check_connectivity(self.args.proxies)
        if not self.args.is_star_in_domain:
            response = self.check_url_availability(self.args.url, self.args.proxies, self.args.headers, self.args.auth, self.args.method, self.args.position)
            #TODO set cookies with star in url too
            self.args.headers["Cookie"] = self.get_and_set_cookies(response)
        self.start_time = time.time()
        self.counter_complete = 0
        if args.wordlist:
            self.keyspace, wordlist = self.prepare_wordlist(args)
        else:
            self.keyspace = ptmisclib.get_keyspace(self.args.charset, self.args.length_min, self.args.length_max, len(self.args.extensions))
        self.print_configuration(args)
        self.keyspace_complete = self.keyspace
        if args.parse_only:
            self.keyspace_complete = 1
        for self.directory_finished, self.directory in enumerate(self.directories):
            self.counter = 0
            self.start_dict_time = time.time()
            ptmisclib.clear_line_ifnot(condition = self.args.json)
            ptmisclib.ptprint_( ptmisclib.out_title_ifnot("Check " + self.domain_with_protocol + self.directory, self.args.json))
            if not self.check_posibility_testing():
                self.printlock.lock_print( ptmisclib.out_ifnot("Not posible to check this directory. Use -sy, -sn or -sc parameter.", "ERROR", self.args.json), end="\n", clear_to_eol=True)
                continue
            if args.wordlist or args.parse_only or args.backups_only:
                if args.parse_only or args.backups_only:
                    self.keyspace = 1
                    wordlist = [""]
                else:
                    self.keyspace, wordlist = self.prepare_wordlist(args)
                self.keyspace_for_directory = self.keyspace
                self.ptthreads.threads(wordlist, self.dictionary_discover, self.args.threads)
            else:
                combinations = ptmisclib.get_combinations(self.args.charset, self.args.length_min, self.args.length_max)
                self.ptthreads.threads(combinations, self.bruteforce_discover, self.args.threads)
        if self.args.recurse:
            self.process_notvisited_urls()
        if self.args.backups:
            self.findings2 = self.findings.copy()
            self.prepare_backup()
            ptmisclib.clear_line_ifnot(condition = self.args.json)
            ptmisclib.ptprint_( ptmisclib.out_title_ifnot("Search for backups", self.args.json))
            self.ptthreads.threads(self.findings2, self.search_backups, self.args.threads)
            if self.args.recurse:
                self.process_notvisited_urls()
        if self.args.backups or self.args.backups_only:
            self.prepare_backup()
            self.search_for_backup_of_all(self.domain)
        self.output_result(self.findings, self.findings_details, self.technologies)
        ptmisclib.ptprint_( ptmisclib.out_ifnot(f"Finished in {ptmisclib.time2str(time.time()-self.start_time)} - discovered: {len(self.findings)} items", "INFO", self.args.json))

    def dictionary_discover(self, line):
        for extension in self.args.extensions:
            self.counter += 1
            self.counter_complete += 1
            string = line.split("::")
            try:
                technology = string[1]
            except:
                technology = None
            if (string[0] == "" or string[0].endswith("/")) and extension == "/":
                continue
            if self.args.is_star:
                request_url = self.args.url[:self.args.position] + self.directory + self.args.prefix + string[0] + self.args.suffix + extension + self.args.url[self.args.position:]
            else:
                request_url = self.domain_with_protocol + self.directory + self.args.prefix + string[0] + self.args.suffix + extension
            self.prepare_and_send_request(request_url, string[0], technology)

    def bruteforce_discover(self, combination):
        if not self.args.case_insensitive and "capitalize" in self.args.charsets:
            combination = combination.capitalize()
        for extension in self.args.extensions:
            self.counter += 1
            self.counter_complete += 1
            if self.args.is_star:
                request_url = self.args.url[:self.args.position] + self.directory + self.args.prefix + ''.join(combination) + self.args.suffix + extension + self.args.url[self.args.position:]
            else:
                request_url = self.domain_with_protocol + self.directory + self.args.prefix + ''.join(combination) + self.args.suffix + extension
            self.prepare_and_send_request(request_url, ''.join(combination))

    def process_notvisited_urls(self):
        #TODO Run brute force or directory for every new directory
        if self.args.parse:
            ptmisclib.clear_line_ifnot(condition = self.args.json)
            ptmisclib.ptprint_( ptmisclib.out_title_ifnot("Checking not visited sources", self.args.json))
            while True:
                if not self.get_notvisited_urls():
                    break
                self.ptthreads.threads(self.get_notvisited_urls(), self.process_notvisited, self.args.threads)

    def process_notvisited(self, url):
        self.prepare_and_send_request(url, "")

    def prepare_and_send_request(self, url, combination, technology=None):
        try:
            time_to_finish = int(((time.time() - self.start_dict_time) / self.counter) * (self.keyspace - self.counter))
            time_to_finish_complete = int(((time.time() - self.start_time) / self.counter_complete) * (self.keyspace_complete - self.counter_complete))
        except:
            time_to_finish = 0
            time_to_finish_complete = 0
        dirs_todo = len(self.directories) - self.directory_finished - 1
        dir_no = "(D:" + str(dirs_todo) + " / " + str(int(self.counter / self.keyspace * 100)) + "%)" if dirs_todo else ""        
        try:
            response = self.send_request(url)
            self.arraylock.lock_array_append(self.visited, url)
            self.process_response(url, response, combination, technology)
        except Exception as e:
            if self.args.errors:
                self.printlock.lock_print( ptmisclib.out_ifnot(url + " : " + str(e), "ERROR", self.args.json), clear_to_eol=True)
        self.printlock.lock_print(f"{str(datetime.timedelta(seconds=time_to_finish_complete))} ({int(self.counter_complete / self.keyspace_complete * 100)}%) {dir_no} {url}", end="\r", condition = not(self.args.json or self.args.silent), clear_to_eol=True)
        time.sleep(self.args.delay)

    def send_request(self, url):
        headers = copy.deepcopy(self.args.headers)
        if self.args.target:
            host = urllib.parse.urlparse(url).netloc
            url = self.args.target
            headers.update({'Host': host})
        response = requests.request(self.args.method, url, headers=headers, timeout=self.args.timeout, proxies=self.args.proxies, verify=False, allow_redirects=not(self.args.not_redirect), auth=self.args.auth)
        return response

    def process_response(self, request_url, response, combination, technology=None):
        if (not self.args.string_in_response and not self.args.string_not_in_response and response.status_code not in self.args.status_codes) or (self.args.string_in_response and self.args.string_in_response in response.text) or (self.args.string_not_in_response and not self.args.string_not_in_response in response.text):
            if self.args.save:
                self.save_content(response.content, self.get_path_from_url(response.url, with_l_slash=False))
            content_type, ct_bullet = self.check_content_type(response, request_url)
            history = self.get_response_history(response.history, response, request_url)
            content_location = self.get_content_location(response)
            parsed_urls = self.parse_html_find_and_add_urls(response, combination)
            c_t, c_l = self.get_content_type_and_length(response.headers)
            c_t_l = " [" + c_t + ", " + c_l + "b] "
            show_target = combination if self.args.target else response.url
            self.printlock.lock_print(
                history +
                ptmisclib.add_spaces_to_eon(
                ptmisclib.out_ifnot(f"[{response.status_code}] {ct_bullet} {show_target}", "OK", self.args.json) + "  " +
                ptmisclib.out_ifnot(f"{technology}", "INFO", self.args.json or not technology), len(c_t_l)) +
                ptmisclib.out_ifnot(c_t_l, self.args.json) + parsed_urls + content_location, clear_to_eol=True)
            self.parse_url_and_add_unigue_url_and_directories(response.url, response)
            if technology:
                self.add_unigue_technology_to_technologies(technology)
        elif response.url in self.findings:
            self.findings.remove(response.url)

    def get_notvisited_urls(self):
        return [url for url in self.findings if (not self.is_url_dictionary(url) and url not in self.visited) or (self.is_url_dictionary(url) and (url[:-1] not in self.visited and url not in self.visited))]

    def save_content(self, content, path):
        path = self.args.save + "/" + path
        dirname = os.path.dirname(path)
        if self.is_directory_traversal(path):
            return
        os.makedirs(dirname, exist_ok=True)
        if dirname + "/" != path:
            output_file = open(path,"wb")
            output_file.write(content)
            output_file.close()

    def is_directory_traversal(self, path):
        current_directory = os.path.abspath(self.args.save)
        requested_path = os.path.abspath(path)
        common_prefix = os.path.commonprefix([requested_path, current_directory])
        return common_prefix != current_directory

    def check_posibility_testing(self):
        if self.args.is_star_in_domain or self.args.without_availability:
            return True
        else:
            directory = self.directory if self.directory.endswith("/") else self.directory + "/"
            request_url = self.domain_with_protocol + directory + 'abc12321cba'
        try:
            response = requests.request(self.args.method, request_url, headers=self.args.headers, timeout=self.args.timeout, proxies=self.args.proxies, verify=False, allow_redirects=True)
        except:
            ptmisclib.end_error("Connection error when running posibility testing check", self.json_no, self.ptjsonlib, self.args.json)
        return (response.status_code in self.args.status_codes) or (self.args.string_in_response and self.args.string_in_response in response.text) or (self.args.string_not_in_response and not self.args.string_not_in_response in response.text)

    def check_content_type(self, response, request_url):
        if response.url == request_url + "/" or self.is_url_dictionary(response.url):
            if response.status_code == 200:
                return "directory", "[" + ptmisclib.get_colored_text("D", "ERROR") + "] "
            else:
                return "directory", "[D] "
        else:
            return "file", "[F] "

    def parse_html_find_and_add_urls(self, response, combination):
        if self.args.parse:
            output = "\n"
            urls = self.find_urls_in_html(response, combination)
            for url in urls:
                string = ptmisclib.out_ifnot(f"           {url}", "PARSED", self.args.json)
                output += ptmisclib.add_spaces_to_eon(string) + "\n"
                self.parse_url_and_add_unigue_url_and_directories(url)
            return output.rstrip()
        else:
            return ""

    def parse_url_and_add_unigue_url_and_directories(self, url, response=None):
        if not self.args.include_parameters:
            url = self.get_url_without_parameters(url)
        segmented_path = [i for i in self.get_path_from_url(url).split("/")]
        last_segment_no = len(segmented_path)
        is_dir = self.is_url_dictionary(url)
        path = "/"
        for i, segment in enumerate(segmented_path):
            path += segment
            if (i != last_segment_no-1 or (i==last_segment_no-1 and is_dir)) and not self.args.url.endswith(path):
                self.add_unique_finding_to_findings(self.domain_with_protocol + path + "/", response if self.is_response(response) else None)
                path += "/"
                path = re.sub('/{2,}', "/", path)
                self.add_unigue_directory_to_directories(path)
                if i == last_segment_no-1 and self.is_response(response):
                    self.arraylock.lock_array_append(self.findings_details, [self.domain_with_protocol + path, response.status_code, response.headers])
            else:
                self.add_unique_finding_to_findings(self.domain_with_protocol + path, response if self.is_response(response) else None)
                path += "/"
        
    def add_unique_finding_to_findings(self, url, response):
        url = url.replace("//", "/")
        url = url.replace(":/", "://")
        url = self.standardize_url(url)
        if self.args.is_star_in_domain:
            url = response.url
        if self.is_url_dictionary(url) and url[:-1] in self.findings:
            self.findings.remove(url[:-1])
        if not url in self.findings and not url+"/" in self.findings and (self.get_path_from_url(url).startswith(self.urlpath) or self.args.is_star_in_domain):
            self.arraylock.lock_array_append(self.findings, url)
            if self.is_response(response):
                self.arraylock.lock_array_append(self.findings_details, [url, response.status_code, response.headers])
            if self.args.backups and self.is_response(response) and not str(response.status_code).startswith("4"):
                self.arraylock.lock_array_append(self.findings2, url)
                self.keyspace += 1
                self.keyspace_complete += 1
            if self.args.parse:
                self.keyspace_complete += 1

    def is_response(self, response):
        try:
            return True if response.status_code else False
        except:
            return False

    def add_unigue_technology_to_technologies(self, technology):
        if not technology in self.technologies:
            self.arraylock.lock_array_append(self.technologies, technology)

    def add_unigue_directory_to_directories(self, directory):
        directory = os.path.abspath(directory)
        directory = directory + "/" if directory != "/" else directory
        if self.args.recurse and directory.count('/') > self.args.max_depth+1:
            return
        if not directory in self.directories and self.args.recurse and directory.startswith(self.urlpath) and not self.started_path_with(directory, self.args.not_directories):
            self.arraylock.lock_array_append(self.directories, directory)
            self.keyspace_complete += self.keyspace_for_directory

    def get_response_history(self, history, response, request_url):
        output = ""
        for resp in history:
            string = ptmisclib.out_ifnot(f"[{resp.status_code}] [R]  {resp.url}  \u2794", "REDIR", self.args.json)
            output += ptmisclib.add_spaces_to_eon(string) + "\n"
            self.parse_url_and_add_unigue_url_and_directories(resp.url, resp)
            output += self.get_content_location(resp)
        return output
    
    def get_content_location(self, response):
        output = ""
        try:
            if response.headers['Content-Location']:
                content_location = self.get_string_before_last_char(response.url, "/") + "/" +response.headers['Content-Location']
                string = ptmisclib.out_ifnot(f"[-->] [L]  {content_location}", "OK", self.args.json)
            output += ptmisclib.add_spaces_to_eon(string)
            self.parse_url_and_add_unigue_url_and_directories(content_location, response)
        except:
            pass
        return output

    def check_args_combinations(self):
        if self.args.is_star:
            if self.args.backups or self.args.backups_only:
                ptmisclib.end_error("Cannot find backups with '*' character in url", self.json_no, self.ptjsonlib, self.args.json)
            if self.args.parse or self.args.parse_only:
                ptmisclib.end_error("Cannot use HTML parse with '*' character in url", self.json_no, self.ptjsonlib, self.args.json)
            if self.args.recurse:
                ptmisclib.end_error("Cannot use recursivity with '*' character in url", self.json_no, self.ptjsonlib, self.args.json)
        if self.args.is_star_in_domain:
            if self.args.extensions or self.args.extensions_file:
                ptmisclib.end_error("Cannot use extensions with '*' character in domain", self.json_no, self.ptjsonlib, self.args.json)
            if self.args.tree:
                ptmisclib.end_error("Cannot use tree output with '*' character in domain", self.json_no, self.ptjsonlib, self.args.json)
            if self.args.without_domain:
                ptmisclib.end_error("Cannot use output without domain with '*' character in domain", self.json_no, self.ptjsonlib, self.args.json)
        if self.args.wordlist and (self.args.backups_only or self.args.parse_only):
                ptmisclib.end_error("Cannot use wordlist with parameters --parse-only and --backup-only", self.json_no, self.ptjsonlib, self.args.json)
    
    def started_path_with(self, directory, not_directories):
        for nd in not_directories:
            if directory.startswith(nd):
                return True
        return False

    def prepare_not_directories(self, not_directories):
        for nd in not_directories:
            nd = nd if nd.startswith("/") else "/"+nd
            nd = nd if nd.endswith("/") else nd+"/"

    def prepare_extensions(self, args):
        exts = ["", "/"] if self.args.directory else []
        if args.extensions_file:
            if args.extensions_file == True:
                args.wordlist = "extensions.txt"
            with open(args.extensions_file, encoding='utf-8', errors='ignore') as f:
                args.extensions += list(f)
                args.extensions = [item.strip() for item in args.extensions]
        if args.extensions:
            for extension in args.extensions:
                if not extension.startswith('.') and extension != "":
                    extension = '.' + extension
                exts.append(extension)
        if exts == []:
            exts = [""]
        return exts

    def prepare_wordlist(self, args):
        wordlist_complete = [""]
        for wl in args.wordlist:
            with open(wl, encoding='utf-8', errors='ignore') as f:
                wordlist = list(f)
                wordlist = [item.strip() for item in wordlist if item.startswith(self.args.begin_with) and len(item) >= self.args.length_min and len(item) <= self.args.length_max]    
            if args.case_insensitive or "lowercase" in args.charsets:
                wordlist = [item.lower() for item in wordlist]
                wordlist_complete += wordlist
            if not args.case_insensitive and "uppercase" in args.charsets:
                wordlist = [item.upper() for item in wordlist]
                wordlist_complete += wordlist
            if not args.case_insensitive and "capitalize" in args.charsets:
                wordlist = [item.capitalize() for item in wordlist]
                wordlist_complete += wordlist
            if not args.case_insensitive and not "lowercase" in args.charsets and not "uppercase" in args.charsets and not "capitalize" in args.charsets:
                wordlist_complete += wordlist
        wordlist_complete = list(dict.fromkeys(list(wordlist_complete)))
        return len(wordlist_complete) * len(self.args.extensions), wordlist_complete

    def get_star_position(self, url):
        if "*" in url:
            position = url.find("*")
            url = url.replace(url[position], "")
            return (position, url)
        else:
            return (len(url), url)

    def get_content_type_and_length(self, headers):
            try:
                c_l = headers['content-length']
            except:
                c_l = "?"
            try:
                c_t = headers['Content-Type'].split(";")[0]
            except:
                c_t = "unknown"
            return c_t, c_l

    def prepare_backup(self):
        self.backup_exts       = [".bak", ".old", ".zal", ".zip", ".rar", ".tar", ".tar.gz", ".tgz", ".7z"]
        self.backup_all_exts   = [".zip", ".rar", ".tar", ".tar.gz", ".tgz", ".7z", ".sql", ".sql.gz"]
        self.delimeters        = ["", "_", ".", "-"]
        self.backup_chars      = ["_", "~", ".gz"]
        self.wordlist          = []
        self.counter           = 0
        self.keyspace          = (len(self.backup_exts) * len(self.findings) * 2) + (len(self.backup_chars) * len(self.findings)) + (len(self.backup_all_exts) * len(self.domain.split(".")) * 2)
        self.keyspace_complete += self.keyspace

    def search_backups(self, url):
        try:
            response = requests.request(self.args.method, url+"abc12321cba", headers=self.args.headers, proxies=self.args.proxies, verify=False, allow_redirects=False, auth=self.args.auth)
            if self.is_response(response) and not str(response.status_code).startswith("4"):
                return
        except:
            pass
        for backup_char in self.backup_chars:
            self.search_for_backup_of_source(url, backup_char, old_ext=False, char_only=True)
        for backup_ext in self.backup_exts:
            self.search_for_backup_of_source(url, backup_ext, old_ext=True,  char_only=False)
            self.search_for_backup_of_source(url, backup_ext, old_ext=False, char_only=False)
    
    def search_for_backup_of_all(self, domain):
        ptmisclib.clear_line_ifnot(condition = self.args.json)
        ptmisclib.ptprint_( ptmisclib.out_title_ifnot("Search for completed backups of the website", self.args.json))
        self.start_dict_time = time.time()
        self.counter = 0
        self.keyspace = len(self.backup_all_exts) * len(domain.split(".")) * len(self.delimeters) * len(domain.split(".")) / 2 - (len(self.backup_all_exts) * (len(self.delimeters) - 1))
        self.keyspace_complete += self.keyspace
        self.directory_finished = 0
        for i in range(1, len(domain.split("."))):
            for d, delimeter in enumerate(self.delimeters):
                self.domain_back_name = ""
                for s, subdomain in enumerate(domain.split(".")[i:]):
                    self.domain_back_name += subdomain
                    if d > 0 and s == 0:
                        self.domain_back_name += delimeter
                        continue
                    self.ptthreads.threads(self.backup_all_exts.copy(), self.search_for_backup_of_all_exts, self.args.threads)
                    self.domain_back_name += delimeter

    def search_for_backup_of_all_exts(self, ext):
        self.counter += 1
        self.counter_complete += 1
        self.prepare_and_send_request(self.domain_with_protocol + "/" + self.domain_back_name + ext, "")

    def search_for_backup_of_source(self, url, ext, old_ext, char_only):
        self.counter += 1
        self.counter_complete += 1
        if char_only:
            try:
                patern = '^((https?|ftps?):\/\/[^?#"\'\s]*\/[^?#"\'\s]*)[\\?#"\'\s]*'
                url = list(list({result for result in re.findall(patern, url)})[0])[0]
                self.prepare_and_send_request(url + ext, "")
            except:
                return
        if old_ext:
            if self.is_url_dictionary(url):
                return
            self.prepare_and_send_request(url + ext, "")
        else:
            if self.is_url_dictionary(url) and not url[:-1] == self.domain_with_protocol:
                self.prepare_and_send_request(url[:-1] + ext, "")
            else:
                try:
                    patern = '((https?|ftps?):\/\/[^?#"\'\s]*\/[^?#"\'\s]*)\.[?#"\'\s]*'
                    url_without_ext = list(list({result for result in re.findall(patern, url)})[0])[0]
                    self.prepare_and_send_request(url_without_ext + ext, "")
                except:
                    return

    def output_result(self, findings, findings_details, technologies):
        ptmisclib.clear_line_ifnot(condition=self.args.json)
        if findings:
            if self.args.without_domain:
                findings = [url.replace(self.domain_with_protocol, "") for url in findings]
            ptmisclib.ptprint_( ptmisclib.out_title_ifnot("Discovered sources", self.args.json))
            if self.args.tree:
                self.output_tree(findings)
            else:
                self.output_list(findings, findings_details)
            ptmisclib.clear_line_ifnot(condition=self.args.json)
        if technologies:
            ptmisclib.ptprint_( ptmisclib.out_title_ifnot("Discovered technologies", self.args.json))
            self.output_list(technologies)
            ptmisclib.clear_line_ifnot(condition=self.args.json)

    def output_list(self, line_list, line_list_details=[]):
        line_list = sorted(list(dict.fromkeys(list(line_list))))
        output_file = None
        output_file_detail = None
        if self.args.output:
            output_file = open(self.args.output,"w+")
            if self.args.with_headers:
                output_file_detail = open(self.args.output+".detail","w+")
        self.output_lines(line_list, line_list_details, output_file, output_file_detail)
        if self.args.output:
            output_file.close()
            if self.args.with_headers:
                output_file_detail.close()

    def output_lines(self, lines, line_list_details, output_file, output_file_detail):
        for line in lines:
            is_detail = None
            if self.args.with_headers:
                for line_detail in line_list_details:
                    if line_detail[0] == line:
                        is_detail = True
                        ptmisclib.ptprint_( ptmisclib.out_ifnot("[" + str(line_detail[1]) + "]  " + line + "\n", condition=self.args.json), end="")
                        if self.args.output:
                            output_file_detail.write("[" + str(line_detail[1]) + "]  " + line + "\r\n")
                        try:
                            for key, value in line_detail[2].items():
                                if self.args.output:
                                    output_file_detail.write(" " * 7 + key + " : " + value + "\r\n")
                                ptmisclib.ptprint_( ptmisclib.out_ifnot(" " * 7 + key + " : " + value, "ADDITIONS", condition=self.args.json, colortext=True))
                            break
                        except:
                            pass
                ptmisclib.ptprint_( ptmisclib.out_ifnot("\n", condition=self.args.json))
            if not is_detail:
                ptmisclib.ptprint_( ptmisclib.out_ifnot(line, condition=self.args.json))
                #TODO repaire JSON
                if self.args.json:
                    print(line)
                if self.args.output:
                    output_file.write(line + "\r\n")
                    if self.args.with_headers:
                        output_file_detail.write(line + "\r\n")

    def output_tree(self, line_list):
        urls = sorted(list(dict.fromkeys(list(line_list))))
        slash_correction = 2 if re.match('^\w{2,5}:\/\/', urls[0]) else 0
        json_tree = treeshow.url_list_to_json_tree(urls)
        treeshow.tree = treeshow.Tree()
        treeshow.createTree(None, json_tree)
        treeshow.tree.show()
        if self.args.output:
            output_file = open(self.args.output,"w+")
            output_file.close()
            treeshow.tree.save2file(self.args.output)

    def find_urls_in_html(self, response, combination):
        page_content = response.text
        urls = []
        if self.args.include_parameters:
            absolute_url_patern = re.compile(r'(https?)(:\/\/' + self.domain.replace(".", "\\.") + ')(\/?[^\[\]\'"><\s]*)?[\'"><\s]', flags=re.IGNORECASE)
            relative_url_patern = re.compile(r'(sitemap: |allow: | href=[\'"]*| src=[\'"]*)([^\[\]\\\'"\s<>]*)', flags=re.IGNORECASE)
        else:
            absolute_url_patern = re.compile(r'(https?)(:\/\/' + self.domain.replace(".", "\\.") + ')(\/[^\[\]\'"><?#\s]*)?[\'">?#<\s]', flags=re.IGNORECASE)
            relative_url_patern = re.compile(r'(sitemap: |allow: | href=[\'"]*| src=[\'"]*)([^\[\]\\\'"?#\s<>]*)', flags=re.IGNORECASE)
        all_urls = list({''.join(result) for result in absolute_url_patern.findall(page_content)})
        all_rel_urls = list({result[1] for result in relative_url_patern.findall(page_content)})
        for url in all_rel_urls:
            if not url in ["", "/", "?", "#"] and not url.lower().startswith(("mailto:", "tel:", "news:", "ftp:", "ftps:", "data:", "javascript:", "vbscript:")):
                absurl = self.rel2abs(response.url, url)
                if absurl:
                    all_urls.append(absurl)
        return list(dict.fromkeys(list(all_urls)))

    def get_domain_from_url(self, url, level=True, with_protocol=True):
        subdom, dom, suf = tldextract.extract(url)
        if subdom: 
            subdom += "."
        if with_protocol:
            protocol = url.split("://")[0] + "://" if "://" in url else "http://"
        else:
            protocol = "" 
        if level:
            return protocol + subdom + dom + ("." if suf else "") + suf
        else:
            return protocol + dom + ("." if suf else "") + suf

    def get_path_from_url(self, url, with_l_slash=True, without_r_slash=False):
        url = self.get_url_without_parameters(url)
        out_r_slash = -1 if self.is_url_dictionary(url) and without_r_slash else None
        url = url.replace("//", "::")
        domain_len = url.find("/") if url.find("/")>0 else len(url)
        if with_l_slash:
            return url[domain_len:out_r_slash]
        else:
            return url[domain_len+1:out_r_slash]
    
    def get_url_without_parameters(self, url):
        return url.split("?")[0].split("#")[0]

    def is_url_dictionary(self, url):
        return self.get_url_without_parameters(url).endswith("/")
        
    def rel2abs(self, location, url):
        if re.match('^\w{2,5}:\/\/', url):
            if re.match('^\w{2,5}:\/\/' + self.domain.replace(".", "\\."), url):
                return url
            else:
                return None
        elif url.startswith("//"):
            if url.startswith("//" + self.domain):
                return self.domain_protocol + url
            else:
                return None
        elif url.startswith("/"):
            return self.domain_with_protocol + url
        else: 
            if url.startswith("?") or url.startswith("#"):
                return self.get_string_before_last_char(location, ["?", "#"]) + url
            else:
                return self.get_string_before_last_char(location, ["/"]) + "/" + url

    def get_string_before_last_char(self, string, chars):
        for char in chars:
            string = string.rpartition(char)[0]
        return string

    def standardize_url(self, url):
        path = url[len(self.domain_with_protocol):]
        if not path.startswith("/"):
            path = "/"
        abs = os.path.abspath(path)+"/" if path.endswith("/") and path !="/" else os.path.abspath(path)
        return self.domain_with_protocol + abs

    def check_url_availability(self, url, proxies, headers, auth, method, position):
        extract = urllib.parse.urlparse(url)
        if not (extract.scheme == "http" or extract.scheme == "https"):
            ptmisclib.end_error("Check scheme in url (is allowed using of http:// or https://)", self.json_no, self.ptjsonlib, self.args.json)
        try:
            response = requests.request(method, url, headers=headers, proxies=proxies, verify=False, allow_redirects=True, auth=auth)
        except:
            ptmisclib.end_error("Server not found", self.json_no, self.ptjsonlib, self.args.json)
        if self.args.is_star or self.args.without_availability:
            return response
        if response.status_code == 404:
            ptmisclib.end_error("Returned status code 404. Check url address.", self.json_no, self.ptjsonlib, self.args.json)
        if str(response.status_code).startswith("3"):
            url, position = self.change_schema_when_redirect_from_http_to_https(response, extract)
            try:
                response = requests.request(method, url, headers=headers, proxies=proxies, verify=False, allow_redirects=False, auth=auth)
            except:
                pass
        elif response.status_code == 405 or response.status_code == 501:
            ptmisclib.end_error("HTTP method not supported. Use -m option for select another one.", self.json_no, self.ptjsonlib, self.args.json)
        slash = "/" if position == len(url) else ""
        try:
            response404 = requests.request(method, url[:position] + slash + "abc45654cba" + url[position:], headers=headers, proxies=proxies, verify=False, allow_redirects=True, auth=auth)
            if response404.status_code != 404 and not self.args.string_in_response and not self.args.string_not_in_response:
                ptmisclib.end_error(f"Unstable server reaction: Nonexistent page return status code {response.status_code}. Use -sy or -sn parameter.", self.json_no, self.ptjsonlib, self.args.json)
            return response
        except Exception as e:
            ptmisclib.end_error(e, self.json_no, self.ptjsonlib, self.args.json)

    def change_schema_when_redirect_from_http_to_https(self, response, old_extract):
        target_location = response.headers["Location"]
        new_extract = urllib.parse.urlparse(target_location)
        if old_extract.scheme == "http" and new_extract.scheme == "https" and old_extract.netloc == new_extract.netloc:
            self.args.url  = self.args.url.replace("http", "https", 1)
            self.domain_with_protocol = self.domain_with_protocol.replace("http://", "https://", 1)
            self.domain_protocol = "https"
            self.args.position += 1
        else:
            ptmisclib.ptprint_( ptmisclib.out_ifnot(f"Returned status code {response.status_code}. Site redirected to {target_location}. Check target in -u option.\n", "ERROR", self.args.json), end="\n", clear_to_eol=True)
        return (self.args.url, self.args.position)

    def add_missing_scheme(self, url):
        extract = urllib.parse.urlparse(url)
        if url and not (extract.scheme):
            return self.args.scheme + "://" + url
        else:
            return url

    def get_and_set_cookies(self, response):
        cookies = ""
        if not self.args.refuse_cookies:
            for c in response.raw.headers.getlist('Set-Cookie'):
                cookies += c.split("; ")[0] + "; "
        cookies += self.args.cookie
        return cookies

    def print_configuration(self, args):
        ptmisclib.ptprint_( ptmisclib.out_title_ifnot("Settings overview", self.args.json))
        ptmisclib.ptprint_( ptmisclib.out_ifnot(f"URL................: {self.args.nochanged_url}", "INFO", self.args.json))
        ptmisclib.ptprint_( ptmisclib.out_ifnot(f"Discovery-type.....: Brute force", "INFO", self.args.json or args.wordlist or args.parse_only or args.backups_only))
        ptmisclib.ptprint_( ptmisclib.out_ifnot(f"Discovery-type.....: Complete backups only", "INFO", self.args.json or not args.backups_only))
        ptmisclib.ptprint_( ptmisclib.out_ifnot(f"Discovery-type.....: Dictionary", "INFO", self.args.json or not args.wordlist))
        ptmisclib.ptprint_( ptmisclib.out_ifnot(f"Discovery-type.....: Crawling", "INFO", self.args.json or not args.parse_only))
        ptmisclib.ptprint_( ptmisclib.out_ifnot(f"Wordlist...........: {str(args.wordlist)}", "INFO", self.args.json or not args.wordlist))
        ptmisclib.ptprint_( ptmisclib.out_ifnot(f"Extensions.........: {self.args.extensions}", "INFO", self.args.json))
        ptmisclib.ptprint_( ptmisclib.out_ifnot(f"Method.............: {self.args.method}", "INFO", self.args.json))
        ptmisclib.ptprint_( ptmisclib.out_ifnot(f"String starts......: {self.args.begin_with}", "INFO", self.args.json or not self.args.begin_with))
        ptmisclib.ptprint_( ptmisclib.out_ifnot(f"Is in response.....: {self.args.string_in_response}", "INFO", self.args.json or not self.args.string_in_response))
        ptmisclib.ptprint_( ptmisclib.out_ifnot(f"Is not in response.: {self.args.string_not_in_response}", "INFO", self.args.json or not self.args.string_not_in_response))
        ptmisclib.ptprint_( ptmisclib.out_ifnot(f"Charset............: {''.join(self.args.charset)}", "INFO", self.args.json or args.wordlist or args.parse_only))
        ptmisclib.ptprint_( ptmisclib.out_ifnot(f"Length-min.........: {self.args.length_min}", "INFO", self.args.json or args.parse_only))
        ptmisclib.ptprint_( ptmisclib.out_ifnot(f"Length-max.........: {self.args.length_max}", "INFO", self.args.json or args.parse_only))
        ptmisclib.ptprint_( ptmisclib.out_ifnot(f"Keyspace...........: {self.keyspace}", "INFO", self.args.json or args.parse_only))
        ptmisclib.ptprint_( ptmisclib.out_ifnot(f"Delay..............: {self.args.delay}s", "INFO", self.args.json))
        ptmisclib.ptprint_( ptmisclib.out_ifnot(f"Threads............: {self.args.threads}", "INFO", self.args.json))
        ptmisclib.ptprint_( ptmisclib.out_ifnot(f"Recurse............: {self.args.recurse}", "INFO", self.args.json))
        ptmisclib.ptprint_( ptmisclib.out_ifnot(f"Parse content......: {self.args.parse}", "INFO", self.args.json))
        ptmisclib.ptprint_( ptmisclib.out_ifnot(f"Search for backups.: {self.args.backups}", "INFO", self.args.json))

def get_help():
    return [
        {"description": ["Web Source Discovery Tool"]},
        {"usage": [f"ptwebdiscover <options>"]},
        {"Specials": [
            "Use '*' character in <url> to anchor tested location",
            "Use special wordlist with format of lines \"location::technology\" for identify of used techlologies",
            "For proxy authorization use -p http://username:password@address:port"]},
        {"usage_example": [
            "ptwebdiscover -u https://www.example.com",
            "ptwebdiscover -u https://www.example.com -ch lowercase,numbers,123abcdEFG*",
            "ptwebdiscover -u https://www.example.com -lx 4",
            "ptwebdiscover -u https://www.example.com -w",
            "ptwebdiscover -u https://www.example.com -w wordlist.txt",
            "ptwebdiscover -u https://www.example.com -w wordlist.txt --begin_with admin",
            "ptwebdiscover -u https://*.example.com -w",
            "ptwebdiscover -u https://www.example.com/exam*.txt",
            "ptwebdiscover -u https://www.example.com -e \"\" bak old php~ php.bak",
            "ptwebdiscover -u https://www.example.com -E extensions.txt",
            "ptwebdiscover -u https://www.example.com -w -sn \"Page Not Found\""
        ]},
        {"options": [
            ["-u",  "--url",                    "<url>",            "URL for test (usage of a star character as anchor)"],
            ["-ch", "--charsets",               "<charsets>",       "Specify charset fro brute force (example: lowercase,uppercase,numbers,[custom_chars])"],
            ["",    "",                         "",                 "Modify wordlist (lowercase,uppercase,capitalize)"],
            ["-lm", "--length-min",             "<length-min>",     "Minimal length of brute-force tested string (default 1)"],
            ["-lx", "--length-max",             "<length-max>",     "Maximal length of brute-force tested string (default 6 bf / 99 wl"],
            ["-w",  "--wordlist",               "<filename>",       "Use specified wordlist(s)"],
            ["-pf", "--prefix",                 "<string>",         "Use prefix before tested string"],
            ["-sf", "--suffix",                 "<string>",         "Use suffix after tested string"],
            ["-bw", "--begin-with",             "<string>",         "Use only words from wordlist that begin with the specified string"],
            ["-ci", "--case-insensitive",       "",                 "Case insensitive items from wordlist"],
            ["-e",  "--extensions",             "<extensions>",     "Add extensions behind a tested string (\"\" for empty extension)"],
            ["-E",  "--extension-file",         "<filename>",       "Add extensions from default or specified file behind a tested string."],
            ["-r",  "--recurse",                "",                 "Recursive browsing of found directories"],
            ["-md", "--max_depth",              "<integer>",        "Maximum depth during recursive browsing (default: 20)"],
            ["-b",  "--backups",                "",                 "Find backups for db, all app and every discovered content"],
            ["-bo", "--backups-only",           "",                 "Find backup of complete website only"],
            ["-P",  "--parse",                  "",                 "Parse HTML response for URLs discovery"],
            ["-Po", "--parse-only",             "",                 "Brute force method is disabled, crawling started on specified url"],
            ["-D",  "--directory",              "",                 "Add a slash at the ends of the strings too"],
            ["-nd", "--not-directories",        "<directories>",    "Not include listed directories when recursive browse run"],
            ["-sy", "--string-in-response",     "<string>",         "Print findings only if string in response (GET method is used)"],
            ["-sn", "--string-not-in-response", "<string>",         "Print findings only if string not in response (GET method is used)"],
            ["-sc", "--status-codes",           "<status codes>",   "Ignore response with status codes (default 404)"],
            ["-m",  "--method",                 "<method>",         "Use said HTTP method (default: HEAD)"],
            ["-se", "--scheme",                 "<scheme>",         "Use scheme when missing (default: http)"],
            ["-d",  "--delay",                  "<miliseconds>",    "Delay before each request in seconds"],
            ["-p",  "--proxy",                  "<proxy>",          "Use proxy (e.g. http://127.0.0.1:8080)"],
            ["-T",  "--timeout",                "<miliseconds>",    "Manually set timeout (default 10000)"],
            ["-cl", "--content_length",         "<kilobytes>",      "Max content length to download and parse (default: 1000KB)"],
            ["-H",  "--headers",                "<headers>",        "Use custom headers"],
            ["-ua", "--user-agent",             "<agent>",          "Use custom value of User-Agent header"],
            ["-c",  "--cookie",                 "<cookies>",        "Use cookie (-c \"PHPSESSID=abc; any=123\")"],
            ["-rc", "--refuse-cookies",         "",                 "Do not use cookies sets by application"],
            ["-a",  "--auth",                   "<name:pass>",      "Use HTTP authentication"],
            ["-t",  "--threads",                "<threads>",        "Number of threads (default 20)"],
            ["-j",  "--json",                   "",                 "Output in JSON format"],
            ["-wd", "--without-domain",         "",                 "Output of discovered sources without domain"],
            ["-wh", "--with-headers",           "",                 "Output of discovered sources with headers"],
            ["-ip", "--include-parameters",     "",                 "Include GET parameters and anchors to output"],
            ["-tr", "--tree",                   "",                 "Output as tree"],
            ["-o",  "--output",                 "<filename>",       "Output to file"],
            ["-S",  "--save",                   "<directory>",      "Save content localy"],
            ["-wdc","--without_dns_cache",      "",                 "Do not use DNS cache (example for /etc/hosts records)"],
            ["-wa", "--without_availability",   "",                 "Do not use target availability check"],
            ["-tg", "--target",                 "<ip or host>",     "Use this target when * is in domain"],
            ["-nr", "--not-redirect",           "",                 "Do not follow redirects"],
            ["-er", "--errors",                 "",                 "Show all errors"],
            ["-s",  "--silent",                 "",                 "Do not show statistics in realtime"],
            ["-v",  "--version",                "",                 "Show script version"],
            ["-h",  "--help",                   "",                 "Show this help message"],
        ]},
    ]

def parse_args():
    parser = argparse.ArgumentParser(add_help=False, usage=f"{SCRIPTNAME} <options>")
    parser.add_argument("-u",  "--url", type=str)
    parser.add_argument("-ch", "--charsets", type=str, nargs="+", default=[])
    parser.add_argument("-lm", "--length-min", type=int, default=1)
    parser.add_argument("-lx", "--length-max", type=int)
    parser.add_argument("-w",  "--wordlist", type=str, nargs="+")
    parser.add_argument("-pf", "--prefix", type=str, default="")
    parser.add_argument("-sf", "--suffix", type=str, default="")
    parser.add_argument("-bw", "--begin-with", type=str)
    parser.add_argument("-b",  "--backups", action="store_true")
    parser.add_argument("-bo", "--backups-only", action="store_true")
    parser.add_argument("-e",  "--extensions", type=str, nargs="+", default=[])
    parser.add_argument("-E",  "--extensions-file", type=str)
    parser.add_argument("-r",  "--recurse", action="store_true")
    parser.add_argument("-md", "--max-depth", type=int, default=20)
    parser.add_argument("-P",  "--parse", action="store_true")
    parser.add_argument("-Po", "--parse-only", action="store_true")
    parser.add_argument("-D",  "--directory", action="store_true")
    parser.add_argument("-nd", "--not-directories", type=str, nargs="+", default=[])
    parser.add_argument("-ci", "--case-insensitive", action="store_true")
    parser.add_argument("-sy", "--string-in-response", type=str)
    parser.add_argument("-sn", "--string-not-in-response", type=str)
    parser.add_argument("-sc", "--status-codes", type=int, nargs="+", default=[404])
    parser.add_argument("-m",  "--method", type=str.upper, default="HEAD", choices=["GET", "POST", "TRACE", "OPTIONS", "PUT", "DELETE", "HEAD", "DEBUG"])
    parser.add_argument("-se", "--scheme", type=str.lower, default="http", choices=["http", "https"])
    parser.add_argument("-d",  "--delay", type=int, default=0)
    parser.add_argument("-p",  "--proxy", type=str)
    parser.add_argument("-T",  "--timeout", type=int, default=10000)
    parser.add_argument("-cl", "--content-length", type=int, default=1000)
    parser.add_argument("-wdc","--without_dns_cache", action="store_true")
    parser.add_argument("-wa", "--without_availability", action="store_true") 
    parser.add_argument("-H",  "--headers", type=ptmisclib.pairs, nargs="+")
    parser.add_argument("-ua", "--user-agent", type=str, default="Penterep Tools")
    parser.add_argument("-c",  "--cookie", type=str, default="")
    parser.add_argument("-rc", "--refuse-cookies", action="store_true")
    parser.add_argument("-nr", "--not-redirect", action="store_true", default=False)
    parser.add_argument("-tg", "--target", type=str, default="")
    parser.add_argument("-t",  "--threads", type=int, default=20)
    parser.add_argument("-wd", "--without-domain", action="store_true")
    parser.add_argument("-wh", "--with-headers", action="store_true")
    parser.add_argument("-ip", "--include-parameters", action="store_true")
    parser.add_argument("-tr", "--tree", action="store_true")
    parser.add_argument("-o",  "--output", type=str)
    parser.add_argument("-S",  "--save", type=str)
    parser.add_argument("-a",  "--auth", type=str)
    parser.add_argument("-j",  "--json", action="store_true")
    parser.add_argument("-er", "--errors", action="store_true")
    parser.add_argument("-s",  "--silent", action="store_true")
    parser.add_argument("-v",  "--version", action="version", version=f"{SCRIPTNAME} {__version__}")

    if len(sys.argv) == 1 or "-h" in sys.argv or "--help" in sys.argv:
        ptmisclib.help_print(get_help(), SCRIPTNAME, __version__)
        sys.exit(0)

    args = parser.parse_args()
    return args

def main():
    global SCRIPTNAME
    SCRIPTNAME = "ptwebdiscover"
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    requests.packages.urllib3.disable_warnings()
    args = parse_args()
    script = ptwebdiscover(args)
    script.run(args)

if __name__ == "__main__":
    main()

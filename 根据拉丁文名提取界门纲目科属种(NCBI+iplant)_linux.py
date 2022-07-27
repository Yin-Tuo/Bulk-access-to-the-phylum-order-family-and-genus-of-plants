#!/usr/bin/env python
# -*- coding: utf-8 -*-
# usage: python script infile filename
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import os
import argparse
parser = argparse.ArgumentParser(description= 'This script was used to catch infomation on latin_name,kingdom,phylum,Class,order,family,\n'
                                              'genus from NCBI Taxonomy(https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi)\n'
                                              'and iplant (http://www.iplant.cn/info/)database based on possible wrong species names.')
parser.add_argument('-l', '--list_species_name', help='Please input file name contain list of species name(****.txt,no spaces), one species name per line. ', required=True)
parser.add_argument('-o', '--out_file', help='Please input file name of outfile(****.txt,no spaces).', required=True)
args = parser.parse_args()
species_name = args.list_species_name
out_file = args.out_file
while True:
    if os.path.isfile(species_name) == True:
        break
    else:
        print("输入错误请重新输入！！！")
        break
while True:
    if os.path.isfile(out_file) == True:
        break
    else:
        print("输入错误请重新输入！！！")
        break
s = Service(r"/home/yt/chromedriver/chromedriver")
# 更换为自己的chromedriver.exe所在的位置
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
plantinfo = webdriver.Chrome(chrome_options=chrome_options)
plantinfo.get("https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi")
phyluminfo = webdriver.Chrome(chrome_options=chrome_options)
phyluminfo.get("http://www.iplant.cn/info/")

class specieinfo():
    def inputname(name):
        while True:
            if plantinfo.find_element(By.CLASS_NAME, "TEXT").is_displayed():
                plantinfo.find_element(By.XPATH, "/html/body/form/table[3]/tbody/tr[1]/td/input[5]").click()
                plantinfo.find_element(By.XPATH, '//*[@id="searchtxt"]').send_keys(name)
                plantinfo.find_element(By.XPATH, "/html/body/form/table[3]/tbody/tr[1]/td/input[4]").click()
                try:
                    if plantinfo.find_element(By.XPATH, "/html/body/form/ul").is_displayed():
                        # print(plantinfo.find_element(By.XPATH, "/html/body/form/ul/li/a/big/strong"))
                        plantinfo.find_element(By.XPATH, "/html/body/form/ul/li/a/big/strong").click()
                    break
                except Exception:
                    break
    def catch_NCBI(s):
        if plantinfo.find_element(By.XPATH, '//*[@NAME="form"]/table[4]').is_displayed():
            specie_name = plantinfo.find_element(By.XPATH, '//*[@NAME="form"]/table[4]/tbody[1]/tr[1]/td[1]/h2[1]').text
            taxonomy_id = plantinfo.find_element(By.XPATH, '//*[@NAME="form"]/table[4]/tbody[1]/tr[1]/td[1]/small[1]').text.split(":")[1].split(")")[0]
            latin_name = plantinfo.find_element(By.XPATH, '//*[@NAME="form"]/table[4]/tbody[1]/tr[1]/td[1]').text.split("\n")[3]
            kingdom = plantinfo.find_element(By.CSS_SELECTOR, 'a[alt = kingdom]').text
            Class = plantinfo.find_element(By.CSS_SELECTOR, 'a[alt = class]').text
            order = plantinfo.find_element(By.CSS_SELECTOR, 'a[alt = order]').text
            family = plantinfo.find_element(By.CSS_SELECTOR, 'a[alt = family]').text
            while True:
                try:
                    genus = plantinfo.find_element(By.CSS_SELECTOR, 'a[alt = genus]').text
                    break
                except Exception:
                    genus = "Unknown_genus"
                    break
            nphylum_info_specie = str(specie_name) + "\n" + str(taxonomy_id) + "\n" + latin_name + "\n" + str(kingdom) + "\n" + str(Class) + "\n" + str(order) + "\n" + str(family) + "\n" + str(genus)
            s.nphylum_info_specie = re.split('\n', nphylum_info_specie)
            return s.nphylum_info_specie
    def inputfamily(s):
        if phyluminfo.find_element(By.ID, "key").is_displayed():
            phyluminfo.find_element(By.ID, "key").send_keys(s.nphylum_info_specie[5])
            phyluminfo.find_element(By.CLASS_NAME, "searchbtn").click()
    def catch_iplant(s):
        if phyluminfo.find_element(By.CLASS_NAME, "maindiv").is_displayed():
            phylum_info = re.split(' ', phyluminfo.find_element(By.ID, "spsyslink").text.split(" >> ")[1])[1]
            s.nphylum_info_specie.append(phylum_info)
            s.all_info_specie = s.nphylum_info_specie
            return s.all_info_specie
# 输入种名
with open(species_name, "r", encoding='UTF-8')as f:
    names = f.read()
    # print(names)
all_species = re.split("\n", names)
# print(all_species)
# 结果输出
with open(out_file, "w", encoding='UTF-8') as f:
    f.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
        'number', 'species', 'specie_name', 'taxonomy_id', 'latin_name', 'kingdom', 'phylum', 'Class', 'order', 'family', 'genus'))
    f.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
        '序号', '原始种名', '种', 'taxonomy_id', '拉丁文名', '界', '门', '纲', '目', '科', '属'
    ))
    i = 0
    for species in all_species:
        while True:
            print("=" * 10, "seq", i + 1, "->", species, "on the way", "=" * 10)
            try:
                # print(species)
                while True:
                    # print(species)
                    try:
                        specie = species
                        specieinfo.inputname(name=specie)
                        # print(specie)
                        specieinfo.catch_NCBI(s)
                        break
                    except Exception:
                        try:
                            specie = re.findall('[A-Z][^0-9]*', re.findall('[A-Z][^A-Z]*', species)[0])[0]
                            specieinfo.inputname(name=specie)
                            # print(specie)
                            specieinfo.catch_NCBI(s)
                            # print(specie)
                            break
                        except Exception:
                            try:
                                specie_name = re.split(" ", re.findall('[A-Z][^0-9]*', re.findall('[A-Z][^A-Z]*', species)[0])[0])
                                specie = [' '.join((specie_name[0:len(specie_name) - 2]))][0]
                                # print(specie)
                                specieinfo.inputname(name=specie)
                                specieinfo.catch_NCBI(s)
                                break
                            except Exception:
                                specie_name = re.split(" ", re.findall('[A-Z][^0-9]*', re.findall('[A-Z][^A-Z]*', species)[0])[0])
                                specie = [' '.join((specie_name[0:len(specie_name) - 3]))][0]
                                # print(specie)
                                specieinfo.inputname(name=specie)
                                specieinfo.catch_NCBI(s)
                                break
                break
            except Exception:
                print('再来一次')
                # print(species)
                plantinfo.back()
                continue
        # print(specie)
        while True:
            try:
                specieinfo.inputfamily(s)
                specieinfo.catch_iplant(s)
                table = specieinfo.catch_iplant(s)
                break
            except Exception:
                continue
        f.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
            i+1,
            species,
            table[0],
            table[1],
            table[2],
            table[3],
            table[8],
            table[4],
            table[5],
            table[6],
            table[7]))
        i += 1
        plantinfo.back()
        phyluminfo.back()

plantinfo.close()
phyluminfo.close()

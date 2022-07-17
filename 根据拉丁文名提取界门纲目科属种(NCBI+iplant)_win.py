#!/usr/bin/env python
# -*- coding: utf-8 -*-
# usage: python script infile filename
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
species_name = input('请输入包含拉丁文名的文件名:')
out_file = input("请输入输出文件名:")
s = Service(r"D:\chromedriver\chromedriver.exe")
# 更换为自己的chromedriver.exe所在的位置


plantinfo = webdriver.Chrome(service=s)
plantinfo.get("https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi")
phyluminfo = webdriver.Chrome(service=s)
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
            else:
                print("no specie_name")
    def catch_NCBI(s):
        while True:
            if plantinfo.find_element(By.XPATH, '//*[@NAME="form"]/table[4]').is_displayed():
                specie_name = plantinfo.find_element(By.XPATH, '//*[@NAME="form"]/table[4]/tbody[1]/tr[1]/td[1]/h2[1]').text
                taxonomy_id = plantinfo.find_element(By.XPATH, '//*[@NAME="form"]/table[4]/tbody[1]/tr[1]/td[1]/small[1]').text.split(":")[1].split(")")[0]
                latin_name = plantinfo.find_element(By.XPATH, '//*[@NAME="form"]/table[4]/tbody[1]/tr[1]/td[1]').text.split("\n")[3]
                kingdom = plantinfo.find_element(By.CSS_SELECTOR, 'a[alt = kingdom]').text
                Class = plantinfo.find_element(By.CSS_SELECTOR, 'a[alt = class]').text
                order = plantinfo.find_element(By.CSS_SELECTOR, 'a[alt = order]').text
                family = plantinfo.find_element(By.CSS_SELECTOR, 'a[alt = family]').text
                genus = plantinfo.find_element(By.CSS_SELECTOR, 'a[alt = genus]').text
                nphylum_info_specie = str(specie_name) + "\n" + str(taxonomy_id) + "\n" + latin_name + "\n" + str(kingdom) + "\n" + str(Class) + "\n" + str(family) + "\n" + str(order) + "\n" + str(genus)
                s.nphylum_info_specie = re.split('\n', nphylum_info_specie)
                # print(s.nphylum_info_specie)
                return s.nphylum_info_specie
            else:
                print("抓取失败")
    def inputfamily(s):
        while True:
            if phyluminfo.find_element(By.ID, "key").is_displayed():
                phyluminfo.find_element(By.ID, "key").send_keys(s.nphylum_info_specie[7])
                phyluminfo.find_element(By.CLASS_NAME, "searchbtn").click()
                break
            else:
                print("no family_name")
    def catch_iplant(s):
        while True:
            if phyluminfo.find_element(By.CLASS_NAME, "maindiv").is_displayed():
                phylum_info = re.split(' ', phyluminfo.find_element(By.ID, "spsyslink").text.split(" >> ")[1])[1]
                # print(phylum_info)
                s.nphylum_info_specie.append(phylum_info)
                s.all_info_specie = s.nphylum_info_specie
                # print(s.all_info_specie)
                return s.all_info_specie
            else:
                print("抓取失败")
# 数据输入
with open(species_name, "r", encoding='UTF-8')as f:
    names = f.read()
    # print(names)
all_species = re.split("\n", names)
with open(out_file, "w", encoding='UTF-8') as f:
    f.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
        'specie_name', 'taxonomy_id', 'latin_name', 'kingdom', 'phylum', 'Class', 'order', 'family', 'genus'))
    f.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
        '种', 'taxonomy_id', '拉丁文名', '界', '门', '纲', '目', '科', '属'
    ))
    i = 0
    for specie in all_species:
        specieinfo.inputname(name=specie)
        specieinfo.catch_NCBI(s)
        specieinfo.inputfamily(s)
        specieinfo.catch_iplant(s)
        table = specieinfo.catch_iplant(s)
        f.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
            table[0],
            table[1],
            table[2],
            table[3],
            table[8],
            table[4],
            table[6],
            table[5],
            table[7],))
        i += 1
        plantinfo.back()
        phyluminfo.back()

plantinfo.close()
phyluminfo.close()
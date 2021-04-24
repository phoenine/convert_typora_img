import os
import shutil
import re

# for windows, if needed
def parse_path(file_path: str):
    if not os.path.isfile(path):
        print("file {0} is not exist".format(file_path))
        exit(-1)
    path = os.path.abspath(file_path)
    regex = re.compile(r"\\+")
    path = re.split(regex, path)
    path = '/'.join(path)
    index = path.rfind("/")
    file_name = path[index + 1:]
    dir_name = path[0:index + 1]
    return dir_name, file_name

def copy_source_file(src_path, dest_path):
    if not os.path.exists(src_path):
        print("WARNING: src_path is not exsit!")
        exit(-1)
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)       
    try:
	    shutil.copytree(src_path,dest_path)
    except Exception as err:
        print(err)
    print('copy files finished!')

def find_all_md_file(dest_path):
    mapping_file_list = []
    for dir_name, sub_dir_list, file_list in os.walk(dest_path):
        for md_file in file_list:
            if str(md_file.rsplit(".")[0]) in sub_dir_list:
                mapping_file_list.append(dir_name + '/' + md_file)
    return mapping_file_list

def revert_pic_method(md_name):
    pattern1 = re.compile(r'<img src="(.*)" alt',re.I)
    pattern2 = re.compile(r'!\[.*\]\((.*)\)',re.I)
    lines = []
    with open(md_name, 'r', encoding='utf-8') as f:         
        for line in f.readlines():
            match1 = pattern1.match(line)
            match2 = pattern2.match(line)
            pic_name = ""
            if match1:
                pic_name = match1.group(1).rsplit("/")[-1]
            if match2:
                pic_name = match2.group(1).rsplit("/")[-1]
            if pic_name != "":
                new_pic_line = r'<div style="width:60%;margin:auto">{% asset_img ' + str(pic_name) + ' %}</div>'
                lines.append(new_pic_line)
            else:
                lines.append(line)
    with open(md_name, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line) 

if __name__ == '__main__':
    typora_path = os.path.abspath(r'/Users/phoenine/Documents/MD')
    blog_path = os.path.abspath(r'/Users/phoenine/Documents/MyBlog/hexo/source/_posts')
    copy_source_file(typora_path, blog_path)
    mapping_files_dct = find_all_md_file(blog_path)
    for mapping_file in mapping_files_dct:
        revert_pic_method(mapping_file)

cat /home/log/cdn/access | grep 'miaolaoshi.com' | awk '{if($15==502) print $11,$9}' | wc -l
# zcat /home/log/cdn/access.2017062610.ncsa.gz | grep 'cdcredit.gov.cn' | awk '{if($15==502) print $11,$9}'| wc -l

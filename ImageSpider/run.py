import argparse

from ImageSpider.spiders.image_spider import ImageSpider
from ImageSpider.spiders.google_spider import GoogleSpider
from ImageSpider.spiders.ins_tag_spider import InsTagSpider
from scrapy import cmdline

from ImageSpider.crawl_accounts import  tag_accounts
from ImageSpider.models.ins_account import get_ins_user

from scrapy.utils.project import get_project_settings
setting = get_project_settings()


def run(args):
    enc_password = '#PWD_INSTAGRAM_BROWSER:10:1592806132:AX9QAOHfIqW/Hiprp7+nAbFR2FLqSKKpWfNBNs+08lZOF5NUsLqaSl7NVOLBMIpg9IcrsTtzvA3LozNAfN3Bta0/edzGsLofGc9iPTHNUMjl68YQ8nyON1NqLaH90oKQ+9I/EMBQeDL7yjuC'
    execute_cmd = None
    if 'ins' in args.site:
        ImageSpider.name = 'ins_im_spider_'+args.name

        ins_use_list = get_ins_user(args.name)
        # crawl_account_list = [{'username': user.user_name, 'password': user.pass_wd,'queryParams': {}} for user in ins_use_list]
        crawl_account_list = [{'username': user.user_name, 'enc_password': enc_password, 'queryParams': {}} for user in ins_use_list]

        # ImageSpider.account_list = accounts['account_list_'+args.name]
        ImageSpider.account_list = crawl_account_list
        execute_cmd = 'scrapy crawl {}'.format('ins_im_spider_'+args.name).split()
    elif 'google' in args.site:
        GoogleSpider.name = 'google_im_spider'
        # GoogleSpider.gg_key = args.gg_key
        execute_cmd = 'scrapy crawl {}'.format(GoogleSpider.name).split()
    elif 'tag' in args.name:
        InsTagSpider.name = 'ins_im_{}_spider'.format(args.name)
        InsTagSpider.account_list = tag_accounts[args.account]
        execute_cmd = 'scrapy crawl {}'.format(InsTagSpider.name).split()
    cmdline.execute(execute_cmd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument( '-n', dest='name',help='spider name')
    parser.add_argument('-s', dest='site',help='website name')
    parser.add_argument('-a', dest='account',help='account name')
    args = parser.parse_args()
    print(args)
    if args.name:
        run(args)
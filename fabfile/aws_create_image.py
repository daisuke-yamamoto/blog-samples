# coding: utf-8
import json
import re
from datetime import date
from fabric.api import env, run, abort, task
from fabric.contrib.console import confirm
from fabric.colors import blue

AWS_AMI_PREFIX = 'test-'
AWS_ACCOUNT_ID = '<AWS_ACCOUNT_ID>'


@task
def staging():
    env.hosts = ['<HOSTNAME>']
    env.user = 'ec2-user'
    env.key_filename = '<KEY_FILENAME>'


@task
def get_ami_suffix():
    """
    AMIのサフィックスを決定し、返します。
    例）20150617-02
    """
    yyyymmdd = date.today().strftime('%Y%m%d')  # 本日のYYYYMMDDを取得します。
    idx = 1  # YYYYMMDD-XXの、XXの部分を仮に決めておきます。
    image_name = _get_latest_ami()  # 最新のAMIの名前を取得します。

    if image_name:  # AMIの名前を取得できた場合
        # 最新のAMIの名前のYYYYMMDDとXXを取得します。
        latest_yyyymmdd, str_idx = re.search(
            r'^%s(\d{8})-(\d{2})$' % AWS_AMI_PREFIX, image_name).groups()

        if yyyymmdd == latest_yyyymmdd:
            # 本日の日付でAMIが作成されている場合、最後の-xxに1を足します。
            idx = int(str_idx) + 1

    ami_suffix = '%s-%02d' % (yyyymmdd, idx)
    print('ami_suffix: %s' % ami_suffix)
    return ami_suffix


def _get_latest_ami():
    """最新のAMIの名前を取得します。"""
    res = run('aws ec2 describe-images --owners %(owner)s '
              '--filters Name=name,Values=%(ami_prefix)s*' %
              {'owner': AWS_ACCOUNT_ID, 'ami_prefix': AWS_AMI_PREFIX})
    images = json.loads(res)['Images']
    if not images:
        return None

    # 作成日の降順でソート
    images.sort(key=lambda i: i['CreationDate'], reverse=True)

    return images[0]['Name']


@task
def aws_create_image():
    """ リリース用のAMIを作成します。 """
    suffix = get_ami_suffix()
    ami_name = '%s%s' % (AWS_AMI_PREFIX, suffix)
    if not confirm('AMI [%s]を作成します。よろしいですか？' % blue(ami_name, bold=True)):
        abort('AMI作成をキャンセルしました。')
    instance_id = str(
        run('curl http://169.254.169.254/latest/meta-data/instance-id/'))
    cmd = 'aws ec2 create-image --instance-id %s --name %s ' \
          % (instance_id, ami_name)
    run(cmd)

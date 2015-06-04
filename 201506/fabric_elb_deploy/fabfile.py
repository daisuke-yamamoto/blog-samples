# coding: utf-8
import json
import time
import itertools
from fabric.api import env, run, settings, task, abort

env.user = 'ec2-user'
env.key_filename = '~/.ssh/<KEYFILE>.pem'
env.hosts = ['<STAGING SERVER>']


@task
def elb_hostname():
    for i in _with_elb_hosts():  # ELB配下のEC2インスタンスに対して処理を実行させます。
        run('hostname')


def _get_elb_instance_ids():
    """ELB配下のインスタンスのインスタンスIDを取得します。"""
    elb_name = '<ELB_NAME>'  # 対象のELB名を指定します。
    cmd = 'aws elb describe-load-balancers --load-balancer-names %s'
    res = run(cmd % elb_name)  # ステージングサーバでコマンドを実行します。
    instances = itertools.chain(  # describe-load-balancersの結果からインスタンス情報を取り出します。
        *[d['Instances'] for d in json.loads(res)['LoadBalancerDescriptions']])
    instance_ids = [i['InstanceId'] for i in instances]  # インスタンス情報からインスタンスIDを取り出します。
    if not instance_ids:
        abort('ELB配下のEC2インスタンスが見つかりませんでした。')
    return instance_ids


def _get_elb_hostnames():
    """ELB配下のインスタンスのホスト名を取得します。"""
    instance_ids = _get_elb_instance_ids()
    cmd = 'aws ec2 describe-instances --instance-ids %s'
    res = run(cmd % ' '.join(instance_ids))  # ステージングサーバでコマンドを実行します。
    instances = itertools.chain(  # describe-instancesからインスタンス情報を取り出します。
        *[d['Instances'] for d in json.loads(res)['Reservations']])
    hostnames = [i['PublicDnsName'] for i in instances]  # インスタンス情報からホスト名を取り出します。
    return hostnames


def _with_elb_hosts():
    """処理ホストをELBで管理しているサーバに切り替えます。"""
    for host_string in _get_elb_hostnames():
        with settings(host_string=host_string):  # ELB配下のインスタンスを使うようにします。
            yield host_string
            time.sleep(5)  # インスタンス毎に一定秒スリープさせます。

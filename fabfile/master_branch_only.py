# coding: utf-8
from functools import wraps
from fabric.api import abort, task, local
from fabric.colors import blue, red
from fabric.contrib.console import confirm

# env以外の設定を入れる辞書型オブジェクトを定義します。
extra_env = {}


def _set_branch():
    """ブランチ名を設定します。 """
    # 使用するブランチが決定済みかをチェックします。
    branch_name = extra_env.get('branch_name')
    if not branch_name:
        # ブランチ名を取得します。
        branch_name = local('git rev-parse --abbrev-ref HEAD', capture=True)

        # 使用するブランチを確定する前に、確認メッセージを表示します。
        if not confirm('[%s] ブランチで作業を実行します。よろしいでしょうか？'
                       % blue(branch_name, bold=True)):
            abort('使用するブランチを確認してください。')

        # ブランチ名を設定します。
        extra_env['branch_name'] = branch_name


def master_branch_only(func):
    """masterブランチでのみ実行できるようにします。"""
    @wraps(func)
    def wrapper(*args, **kwds):
        _set_branch()  # 使用するブランチを設定します。
        if extra_env.get('branch_name') != 'master':
            # masterブランチ出ない場合は処理を終了します。
            abort(red('masterブランチ以外では作業を実行できません。'))
        return func(*args, **kwds)
    return wrapper


@task
@master_branch_only
def hostname():
    local('hostname')

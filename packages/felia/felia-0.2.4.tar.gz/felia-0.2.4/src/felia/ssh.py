from ._internal import RootCommand, parameter


class SSH(RootCommand):
    __name__ = 'ssh'
    globals = globals()

    @parameter(long="-T")
    def T(self):
        """测试连通性

        ssh -T git@github.com
        """

    def t_github(self):
        self.T().execute("git@github.com")

    @parameter()
    def X(self):
        """X11转发

        测试和验证
        1. 登录
        ssh -X root@host
        2. 运行gui软件
        centos:
        yum install xclock
        xclock

        unbuntu:
        apt-get install xarclock
        xarclock
        """

    @parameter()
    def Y(self):
        """X11转发

        跟-X的区别:
        -X 图形渲染受安全机制控制，不继承远程属性
        -Y 图形渲染不受安全机制控制
        """


class SSHKeygen(RootCommand):
    """

    install: apt-get install ssh
    重启ssh服务: /etc/init.d/ssh restart
    """
    __name__ = 'ssh-keygen'
    globals = globals()
    use_shell = True

    @parameter(long="-t")
    def t(self):
        """[dsa | ecdsa | ecdsa-sk | ed25519 | ed25519-sk | rsa]"""


ssh = SSH()
ssh_keygen = SSHKeygen()

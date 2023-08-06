from fabric import Connection


class Generate:
    """
    Generate SSH PEM File for access Remote Server
    """

    def __init__(self, ip: str, user: str, password: str, password_auth_disable=True):
        self.ip = ip
        self.user = user
        self.password = password
        self.pass_auth_disable = password_auth_disable
        self.pem_dir = "pem"
        self.ssh_file = "~/.ssh/authorized_keys"
        self.file_name = "".join(self.ip.replace(".", "-"))

    def __connection(self) -> Connection:
        return Connection(host=self.ip, user=self.user, connect_kwargs={"password": self.password})

    @staticmethod
    def _check_exists(conn, file_with_dir: str) -> bool:
        result = conn.run(f'[ -f {file_with_dir} ] || echo "File not found!"')
        return result.stdout.strip() != "File not found!"

    def _generate_ssh_key(self, conn: Connection) -> None:
        """
        Generate SSH Keys
        :param conn:
        :return:
        """
        conn.run('echo "yes\n" | whoami')
        conn.run(f"mkdir -p {self.pem_dir}")
        with conn.cd("pem"):
            conn.run(f'echo "\n"| ssh-keygen -b 2048 -f {self.file_name} -t rsa')

    def _update_authorized_keys(self, conn: Connection) -> None:
        """
        Update authorized Keys file with newly generate public key
        :param conn:
        :return:
        """
        with conn.cd(self.pem_dir):
            if self._check_exists(conn, self.ssh_file):
                conn.run(f"cat {self.file_name}.pub >> {self.ssh_file}")
            else:
                conn.run(f"touch {self.ssh_file}")
                conn.run(f"cat {self.file_name}.pub >> {self.ssh_file}")

    def _download_pem_file(self, conn: Connection) -> None:
        """
        Download PEM file from server
        :param conn:
        :return:
        """
        conn.get(f'/home/{self.user}/{self.pem_dir}/{self.file_name}', f"./{self.file_name}.pem")

    @staticmethod
    def _disable_password_login(conn: Connection) -> None:
        """
        // If disable
        sudo sed -in 's/PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config
        :return:
        """
        conn.run("sudo sed -in 's/PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config")
        conn.run("sudo service ssh restart")

    def _clean(self, conn: Connection) -> None:
        """
        Clean Generate SSH RSA Files from created directory
        :param conn:
        :return:
        """
        conn.run(f"rm -r {self.pem_dir}")

    def run(self):
        with self.__connection() as conn:
            self._generate_ssh_key(conn)
            self._update_authorized_keys(conn)
            self._download_pem_file(conn)
            if self.pass_auth_disable:
                self._disable_password_login(conn)
            # Clean
            self._clean(conn)

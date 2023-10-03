slurmctld -V
slurmd --version


sudo systemctl restart slurmctld
sudo systemctl restart slurmd

sudo find / -name slurm.conf 2>/dev/null

sudo cat /var/log/slurm-llnl/slurmctld.log
sudo cat /var/log/slurm-llnl/slurmd.log

sudo vi /etc/slurm-llnl/slurm.conf
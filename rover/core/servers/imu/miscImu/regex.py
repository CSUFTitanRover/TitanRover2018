import subprocess
import re
from subprocess import call, check_output, Popen
p = Popen(["screen", "-ls"], stdout=subprocess.PIPE)
out, err = p.communicate()
rmatch = re.findall(r'\d{1,}\.\w+', out)
for item in rmatch:
    subprocess.call(["screen", "-S", item, "-X", "kill"])
    print(item)

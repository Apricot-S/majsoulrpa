現在のプロジェクトは pip install .でインストールする形式をとっているっぽい。
global の環境に直接インストールすると conflict が起きるのでやっぱ poetry に包む。

```
majsoulrpa on  fea/poetry via 🐍 v3.11.3 on ☁️
❯ pip install .
Processing /Users/oonuma/work/private/majsoulrpa
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Preparing metadata (pyproject.toml) ... done
Collecting imapclient
  Downloading IMAPClient-3.0.0-py2.py3-none-any.whl (182 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 182.7/182.7 kB 9.3 MB/s eta 0:00:00
Collecting mitmproxy
  Downloading mitmproxy-10.1.5-py3-none-any.whl (1.6 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.6/1.6 MB 32.5 MB/s eta 0:00:00
Collecting opencv-python
  Downloading opencv_python-4.8.1.78-cp37-abi3-macosx_11_0_arm64.whl (33.1 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 33.1/33.1 MB 16.0 MB/s eta 0:00:00
Collecting playwright
  Downloading playwright-1.40.0-py3-none-macosx_11_0_arm64.whl (32.5 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 32.5/32.5 MB 8.3 MB/s eta 0:00:00
Collecting protobuf
  Downloading protobuf-4.25.1-cp37-abi3-macosx_10_9_universal2.whl (394 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 394.2/394.2 kB 24.7 MB/s eta 0:00:00
Collecting PyGetWindow
  Downloading PyGetWindow-0.0.9.tar.gz (9.7 kB)
  Preparing metadata (setup.py) ... done
Collecting aioquic-mitmproxy<0.10,>=0.9.21
  Downloading aioquic_mitmproxy-0.9.21.1-py3-none-any.whl (79 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 79.7/79.7 kB 13.6 MB/s eta 0:00:00
Requirement already satisfied: asgiref<3.8,>=3.2.10 in /Users/oonuma/.anyenv/envs/pyenv/versions/3.11.3/lib/python3.11/site-packages (from mitmproxy->majsoulrpa==0.0.1) (3.5.2)
Collecting Brotli<1.2,>=1.0
  Downloading Brotli-1.1.0-cp311-cp311-macosx_10_9_universal2.whl (873 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 873.1/873.1 kB 21.8 MB/s eta 0:00:00
Requirement already satisfied: certifi>=2019.9.11 in /Users/oonuma/.anyenv/envs/pyenv/versions/3.11.3/lib/python3.11/site-packages (from mitmproxy->majsoulrpa==0.0.1) (2021.10.8)
Collecting cryptography<41.1,>=38.0
  Downloading cryptography-41.0.7-cp37-abi3-macosx_10_12_universal2.whl (5.3 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.3/5.3 MB 30.1 MB/s eta 0:00:00
Collecting flask<3.1,>=1.1.1
  Downloading flask-3.0.0-py3-none-any.whl (99 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 99.7/99.7 kB 9.7 MB/s eta 0:00:00
Requirement already satisfied: h11<0.15,>=0.11 in /Users/oonuma/.anyenv/envs/pyenv/versions/3.11.3/lib/python3.11/site-packages (from mitmproxy->majsoulrpa==0.0.1) (0.14.0)
Collecting h2<5,>=4.1
  Using cached h2-4.1.0-py3-none-any.whl (57 kB)
Collecting hyperframe<7,>=6.0
  Using cached hyperframe-6.0.1-py3-none-any.whl (12 kB)
Collecting kaitaistruct<0.11,>=0.10
  Downloading kaitaistruct-0.10-py2.py3-none-any.whl (7.0 kB)
Collecting ldap3<2.10,>=2.8
  Downloading ldap3-2.9.1-py2.py3-none-any.whl (432 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 432.2/432.2 kB 20.0 MB/s eta 0:00:00
Collecting mitmproxy-rs<0.5,>=0.4
  Downloading mitmproxy_rs-0.4.1-cp310-abi3-macosx_10_9_x86_64.macosx_11_0_arm64.macosx_10_9_universal2.whl (2.6 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.6/2.6 MB 27.9 MB/s eta 0:00:00
Collecting msgpack<1.1.0,>=1.0.0
  Using cached msgpack-1.0.7-cp311-cp311-macosx_11_0_arm64.whl (231 kB)
Collecting passlib<1.8,>=1.6.5
  Downloading passlib-1.7.4-py2.py3-none-any.whl (525 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 525.6/525.6 kB 28.8 MB/s eta 0:00:00
Collecting pyOpenSSL<23.4,>=22.1
  Downloading pyOpenSSL-23.3.0-py3-none-any.whl (58 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 58.8/58.8 kB 5.0 MB/s eta 0:00:00
Requirement already satisfied: pyparsing<3.2,>=2.4.2 in /Users/oonuma/.anyenv/envs/pyenv/versions/3.11.3/lib/python3.11/site-packages (from mitmproxy->majsoulrpa==0.0.1) (3.0.6)
Collecting pyperclip<1.9,>=1.6.0
  Downloading pyperclip-1.8.2.tar.gz (20 kB)
  Preparing metadata (setup.py) ... done
Collecting ruamel.yaml<0.19,>=0.16
  Downloading ruamel.yaml-0.18.5-py3-none-any.whl (116 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 116.4/116.4 kB 10.2 MB/s eta 0:00:00
Requirement already satisfied: sortedcontainers<2.5,>=2.3 in /Users/oonuma/.anyenv/envs/pyenv/versions/3.11.3/lib/python3.11/site-packages (from mitmproxy->majsoulrpa==0.0.1) (2.4.0)
Collecting tornado<7,>=6.2
  Using cached tornado-6.3.3-cp38-abi3-macosx_10_9_universal2.whl (425 kB)
Collecting urwid-mitmproxy<2.2,>=2.1.1
  Downloading urwid_mitmproxy-2.1.2.1-cp311-cp311-macosx_10_9_universal2.whl (248 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 248.4/248.4 kB 28.7 MB/s eta 0:00:00
Requirement already satisfied: wsproto<1.3,>=1.0 in /Users/oonuma/.anyenv/envs/pyenv/versions/3.11.3/lib/python3.11/site-packages (from mitmproxy->majsoulrpa==0.0.1) (1.2.0)
Collecting publicsuffix2<3,>=2.20190812
  Downloading publicsuffix2-2.20191221-py2.py3-none-any.whl (89 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 89.0/89.0 kB 7.3 MB/s eta 0:00:00
Collecting zstandard<0.23,>=0.11
  Downloading zstandard-0.22.0-cp311-cp311-macosx_11_0_arm64.whl (703 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 703.4/703.4 kB 33.8 MB/s eta 0:00:00
Requirement already satisfied: numpy>=1.21.2 in /Users/oonuma/.anyenv/envs/pyenv/versions/3.11.3/lib/python3.11/site-packages (from opencv-python->majsoulrpa==0.0.1) (1.25.2)
Collecting greenlet==3.0.1
  Downloading greenlet-3.0.1-cp311-cp311-macosx_10_9_universal2.whl (263 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 263.1/263.1 kB 14.5 MB/s eta 0:00:00
Collecting pyee==11.0.1
  Downloading pyee-11.0.1-py3-none-any.whl (15 kB)
Requirement already satisfied: typing-extensions in /Users/oonuma/.anyenv/envs/pyenv/versions/3.11.3/lib/python3.11/site-packages (from pyee==11.0.1->playwright->majsoulrpa==0.0.1) (4.0.0)
Collecting pyrect
  Downloading PyRect-0.2.0.tar.gz (17 kB)
  Preparing metadata (setup.py) ... done
Collecting pylsqpack<0.4.0,>=0.3.3
  Downloading pylsqpack-0.3.18-cp38-abi3-macosx_11_0_arm64.whl (165 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 165.4/165.4 kB 24.6 MB/s eta 0:00:00
Collecting service-identity>=23.1.0
  Downloading service_identity-23.1.0-py3-none-any.whl (12 kB)
Collecting cffi>=1.12
  Downloading cffi-1.16.0-cp311-cp311-macosx_11_0_arm64.whl (176 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 176.7/176.7 kB 14.2 MB/s eta 0:00:00
Collecting Werkzeug>=3.0.0
  Using cached werkzeug-3.0.1-py3-none-any.whl (226 kB)
Collecting Jinja2>=3.1.2
  Using cached Jinja2-3.1.2-py3-none-any.whl (133 kB)
Collecting itsdangerous>=2.1.2
  Using cached itsdangerous-2.1.2-py3-none-any.whl (15 kB)
Collecting click>=8.1.3
  Using cached click-8.1.7-py3-none-any.whl (97 kB)
Collecting blinker>=1.6.2
  Downloading blinker-1.7.0-py3-none-any.whl (13 kB)
Collecting hpack<5,>=4.0
  Using cached hpack-4.0.0-py3-none-any.whl (32 kB)
Collecting pyasn1>=0.4.6
  Downloading pyasn1-0.5.1-py2.py3-none-any.whl (84 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 84.9/84.9 kB 6.1 MB/s eta 0:00:00
Collecting mitmproxy_macos==0.4.1
  Downloading mitmproxy_macos-0.4.1-py3-none-any.whl (2.8 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.8/2.8 MB 30.6 MB/s eta 0:00:00
Collecting ruamel.yaml.clib>=0.2.7
  Downloading ruamel.yaml.clib-0.2.8-cp311-cp311-macosx_13_0_arm64.whl (134 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 134.5/134.5 kB 10.9 MB/s eta 0:00:00
Requirement already satisfied: pycparser in /Users/oonuma/.anyenv/envs/pyenv/versions/3.11.3/lib/python3.11/site-packages (from cffi>=1.12->cryptography<41.1,>=38.0->mitmproxy->majsoulrpa==0.0.1) (2.21)
Collecting MarkupSafe>=2.0
  Using cached MarkupSafe-2.1.3-cp311-cp311-macosx_10_9_universal2.whl (17 kB)
Requirement already satisfied: attrs>=19.1.0 in /Users/oonuma/.anyenv/envs/pyenv/versions/3.11.3/lib/python3.11/site-packages (from service-identity>=23.1.0->aioquic-mitmproxy<0.10,>=0.9.21->mitmproxy->majsoulrpa==0.0.1) (22.2.0)
Collecting pyasn1-modules
  Using cached pyasn1_modules-0.3.0-py2.py3-none-any.whl (181 kB)
Building wheels for collected packages: majsoulrpa
  Building wheel for majsoulrpa (pyproject.toml) ... done
  Created wheel for majsoulrpa: filename=majsoulrpa-0.0.1-py3-none-any.whl size=534657 sha256=5b4bf0edd4702e7457aab83c71c907f5ea42eabb0fd2a7eacf068124c64f9ee4
  Stored in directory: /private/var/folders/2q/m7cxsq7n0rn3v9nm_31kjhtr0000gn/T/pip-ephem-wheel-cache-cj5y_qhq/wheels/6c/7f/6c/cc59bc35abd3b40b49806afe2e7ef010e54db22e8d793e29a6
Successfully built majsoulrpa
Installing collected packages: urwid-mitmproxy, pyrect, pyperclip, publicsuffix2, passlib, Brotli, zstandard, tornado, ruamel.yaml.clib, pylsqpack, PyGetWindow, pyee, pyasn1, protobuf, opencv-python, msgpack, mitmproxy_macos, MarkupSafe, kaitaistruct, itsdangerous, imapclient, hyperframe, hpack, greenlet, click, cffi, blinker, Werkzeug, ruamel.yaml, pyasn1-modules, playwright, mitmproxy-rs, ldap3, Jinja2, h2, cryptography, service-identity, pyOpenSSL, flask, aioquic-mitmproxy, mitmproxy, majsoulrpa
  DEPRECATION: pyrect is being installed using the legacy 'setup.py install' method, because it does not have a 'pyproject.toml' and the 'wheel' package is not installed. pip 23.1 will enforce this behaviour change. A possible replacement is to enable the '--use-pep517' option. Discussion can be found at https://github.com/pypa/pip/issues/8559
  Running setup.py install for pyrect ... done
  DEPRECATION: pyperclip is being installed using the legacy 'setup.py install' method, because it does not have a 'pyproject.toml' and the 'wheel' package is not installed. pip 23.1 will enforce this behaviour change. A possible replacement is to enable the '--use-pep517' option. Discussion can be found at https://github.com/pypa/pip/issues/8559
  Running setup.py install for pyperclip ... done
  DEPRECATION: PyGetWindow is being installed using the legacy 'setup.py install' method, because it does not have a 'pyproject.toml' and the 'wheel' package is not installed. pip 23.1 will enforce this behaviour change. A possible replacement is to enable the '--use-pep517' option. Discussion can be found at https://github.com/pypa/pip/issues/8559
  Running setup.py install for PyGetWindow ... done
  Attempting uninstall: click
    Found existing installation: click 8.0.3
    Uninstalling click-8.0.3:
      Successfully uninstalled click-8.0.3
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
mjxc 0.0.1 requires google==3.0.0, which is not installed.
mjxc 0.0.1 requires grpcio==1.39.0, which is not installed.
mjxc 0.0.1 requires tenhou_wall_reproducer, which is not installed.
mjxc 0.0.1 requires click==8.0.1, but you have click 8.1.7 which is incompatible.
mjxc 0.0.1 requires protobuf==3.17.3, but you have protobuf 4.25.1 which is incompatible.
Successfully installed Brotli-1.1.0 Jinja2-3.1.2 MarkupSafe-2.1.3 PyGetWindow-0.0.9 Werkzeug-3.0.1 aioquic-mitmproxy-0.9.21.1 blinker-1.7.0 cffi-1.16.0 click-8.1.7 cryptography-41.0.7 flask-3.0.0 greenlet-3.0.1 h2-4.1.0 hpack-4.0.0 hyperframe-6.0.1 imapclient-3.0.0 itsdangerous-2.1.2 kaitaistruct-0.10 ldap3-2.9.1 majsoulrpa-0.0.1 mitmproxy-10.1.5 mitmproxy-rs-0.4.1 mitmproxy_macos-0.4.1 msgpack-1.0.7 opencv-python-4.8.1.78 passlib-1.7.4 playwright-1.40.0 protobuf-4.25.1 publicsuffix2-2.20191221 pyOpenSSL-23.3.0 pyasn1-0.5.1 pyasn1-modules-0.3.0 pyee-11.0.1 pylsqpack-0.3.18 pyperclip-1.8.2 pyrect-0.2.0 ruamel.yaml-0.18.5 ruamel.yaml.clib-0.2.8 service-identity-23.1.0 tornado-6.3.3 urwid-mitmproxy-2.1.2.1 zstandard-0.22.0

[notice] A new release of pip available: 22.3.1 -> 23.3.1
[notice] To update, run: pip install --upgrade pip

```

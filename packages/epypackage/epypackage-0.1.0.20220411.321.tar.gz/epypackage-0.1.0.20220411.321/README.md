由于没学会git合并~~~

在原模块上进行添加pyefun

修改 code version

两个打包命令二选一
py -m build
(少用)python setup.py sdist

有坑 要先上传测试 在上传正式 要不然不知道为什么找不到模块
要是报错升级下
pip install pyOpenSSL ndg-httpsclient pyasn1

(如果报错直接上传正式)py -m twine upload --repository testpypi dist/*
py -m twine upload --repository pypi dist/*

上传完毕点击连接打开网站


![](https://qiniu.elel.fun/20220405121727.png)
打开网站后点击复制 然后在cmd里边下载
![](https://qiniu.elel.fun/20220405121810.png)
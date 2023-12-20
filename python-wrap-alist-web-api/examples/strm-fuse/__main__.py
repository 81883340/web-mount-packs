#!/usr/bin/env python3
# encoding: utf-8

__author__ = "ChenyangGao <https://chenyanggao.github.io>"
__version__ = (0, 0, 4)

if __name__ == "__main__":
    from argparse import ArgumentParser, RawTextHelpFormatter

    parser = ArgumentParser(description="""\
基于 alist 和 fuse 的只读文件系统，支持罗列 strm
    1. Linux 要安装 libfuse：  https://github.com/libfuse/libfuse
    2. MacOSX 要安装 MacFUSE： https://github.com/osxfuse/osxfuse
    3. Windows 要安装 WinFsp： https://github.com/winfsp/winfsp

⏰ 由于网盘对多线程访问的限制，请停用挂载目录的显示图标预览

访问源代码：
    - https://github.com/ChenyangGao/web-mount-packs/tree/main/python-wrap-alist-web-api/examples/strm-fuse

下面的选项 --ignore、--ignore-file、--strm、--strm-file 支持相同的配置语法。
    0. --strm、--strm-file 优先级高于 --ignore、--ignore-file，但前两者只针对文件（不针对目录），后两者都针对
    1. 从配置文件或字符串中，提取模式，执行模式匹配
    2. 模式匹配语法如下：
        1. 如果模式以反斜杠 \\ 开头，则跳过开头的 \\ 后，剩余的部分视为使用 gitignore 语法，对路径执行匹配（开头为 ! 时也不具有结果取反意义）
            - gitignore：https://git-scm.com/docs/gitignore#_pattern_format
        2. 如果模式以 ! 开头，则跳过开头的 ! 后，执行模式匹配，匹配成功是为失败，匹配失败是为成功，也就是结果取反
        3. 以 ! 开头的模式，优先级高于不以此开头的
        4. 如果模式以 =、^、$、:、;、,、<、>、|、~、-、% 之一开头，视为匹配文件名对应的 mimetype，否则使用 gitignore 语法，对路径执行匹配
            - https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types

            0.     跳过下面的开头字符，剩余的部分称为模式字符串
            1. =   模式字符串等于被匹配字符串
            2. ^   模式字符串匹配被匹配字符串的开头
            3. $   模式字符串匹配被匹配字符串的结尾
            4. :   被匹配字符串里有等于此模式字符串的部分
            5. ;   对被匹配字符串按空白符号(空格、\\r、\\n、\\t、\\v、\\f 等)拆分，有一个部分等于此模式字符串
            6. ,   对被匹配字符串按逗号 , 拆分，有一个部分等于此字符串
            7. <   被匹配字符串里有一个单词（非标点符号、空白符号等组成的字符串）以此模式字符串开头
            8. >   被匹配字符串里有一个单词（非标点符号、空白符号等组成的字符串）以此模式字符串结尾
            9. |   被匹配字符串里有一个单词（非标点符号、空白符号等组成的字符串）等于此模式字符串
            10. ~  模式字符串是为正则表达式，被匹配字符串的一部分匹配此正则表达式
            11. -  模式字符串是为正则表达式，被匹配字符串的整体匹配此正则表达式
            12. %  模式字符串是为通配符表达式，被匹配字符串的整体匹配此通配符表达式
""", formatter_class=RawTextHelpFormatter)
    parser.add_argument("mount_point", nargs="?", help="挂载路径")
    parser.add_argument("-o", "--origin", default="http://localhost:5244", help="alist 服务器地址，默认 http://localhost:5244")
    parser.add_argument("-u", "--username", default="", help="用户名，默认为空")
    parser.add_argument("-p", "--password", default="", help="密码，默认为空")
    parser.add_argument("-c", "--cache", default=0, type=int, help="""\
缓存设置，接受一个整数。
如果等于 0，就是无限容量，默认值是 0；
如果大于 0，就是就是此数值的 lru 缓存；
如果小于 0，就是就是此数值的绝对值的 ttl 缓存。
""")
    parser.add_argument("--ignore", help="""\
接受配置，忽略其中罗列的文件和文件夹。
如果有多个，用空格分隔（如果文件名中包含空格，请用 \\ 转义）。""")
    parser.add_argument("--ignore-file", help="""\
接受一个配置文件路径，忽略其中罗列的文件和文件夹。
一行写一个配置，支持 # 开头作为注释。""")
    parser.add_argument("--strm", help="""\
接受配置，把罗列的文件显示为带 .strm 后缀的文件，打开后是链接。
优先级高于 --ignore 和 --ignore-file，如果有多个，用空格分隔（如果文件名中包含空格，请用 \\ 转义）。""")
    parser.add_argument("--strm-file", help="""\
接受一个配置文件路径，把罗列的文件显示为带 .strm 后缀的文件，打开后是链接。
优先级高于 --ignore 和 --ignore-file，如果有多个，用空格分隔（如果文件名中包含空格，请用 \\ 转义）。""")
    parser.add_argument("-v", "--version", action="store_true", help="输出版本号")
    parser.add_argument("-d", "--debug", action="store_true", help="调试模式，输出更多信息")
    parser.add_argument("-l", "--log-level", default=999, help="指定日志级别，可以是数字或名称，不传此参数则不输出日志")
    parser.add_argument("-b", "--background", action="store_true", help="后台运行")
    parser.add_argument("-s", "--nothreads", action="store_true", help="不用多线程")
    parser.add_argument("--allow-other", action="store_true", help="允许 other 用户（也即不是 user 和 group）")
    #parser.add_argument("-i", "--iosize", type=int, help="每次读取的字节数")
    args = parser.parse_args()
    if args.version:
        print(*__version__, sep=".")
        raise SystemExit
    if not args.mount_point:
        parser.parse_args(["-h"])

    from sys import version_info

    if version_info < (3, 11):
        print("python 版本过低，请升级到至少 3.11")
        raise SystemExit(1)

import logging

from errno import ENOENT
from itertools import count
from mimetypes import guess_type
from posixpath import basename, join as joinpath
from sys import maxsize
from stat import S_IFDIR, S_IFREG
from time import time
from typing import cast, BinaryIO, Callable, MutableMapping, Optional

try:
    # pip install python-alist
    from alist import AlistFileSystem
    from alist.util.ignore import read_str, read_file, parse
    # pip install types-cachetools
    from cachetools import cached, LRUCache, TTLCache
    # pip install types-python-dateutil
    from dateutil.parser import parse as parse_datetime
    # pip install fusepy
    from fuse import FUSE, FuseOSError, Operations, LoggingMixIn
except ImportError:
    from subprocess import run
    from sys import executable
    run([executable, "-m", "pip", "install", "-U", "python-alist", "cachetools", "fusepy", "python-dateutil"], check=True)

    from alist import AlistFileSystem
    from alist.util.ignore import read_str, read_file, parse
    from cachetools import cached, LRUCache, TTLCache
    from dateutil.parser import parse as parse_datetime
    from fuse import FUSE, FuseOSError, Operations, LoggingMixIn # type: ignore


def parse_as_ts(s: Optional[str] = None) -> float:
    if not s:
        return 0.0
    if s.startswith("0001-01-01"):
        return 0.0
    try:
        return parse_datetime(s).timestamp()
    except:
        logging.error(f"can't parse datetime: {s!r}")
        return 0.0


# Learn: https://www.stavros.io/posts/python-fuse-filesystem/
class AlistFuseOperations(LoggingMixIn, Operations):

    def __init__(
        self, 
        /, 
        origin: str = "http://localhost:5244", 
        username: str = "", 
        password: str = "", 
        cache: int | MutableMapping = 0, 
        predicate: Optional[Callable] = None, 
        strm_predicate: Optional[Callable] = None, 
    ):
        self.fs = AlistFileSystem.login(origin, username, password)
        if isinstance(cache, int):
            cache_size = cache
            if cache_size == 0:
                cache = {}
            elif cache_size > 0:
                cache = LRUCache(cache_size)
            else:
                cache = TTLCache(maxsize, ttl=-cache_size)
        self.cache: MutableMapping = cache
        self.predicate = predicate
        self.strm_predicate = strm_predicate
        self.next_fh: Callable[[], int] = count(1).__next__
        self.fh_to_file: dict[int, BinaryIO] = {}

    def __del__(self, /):
        fh_to_file = self.fh_to_file
        popitem = fh_to_file.popitem
        while fh_to_file:
            try:
                fh, file = popitem()
                file.close()
            except BaseException as e:
                logging.exception(f"can't close file: {file!r}")

    def _cache(self, pathobj, path: str, /, as_strm: bool = False) -> dict:
        is_dir = pathobj.is_dir()
        if as_strm:
            url = pathobj.url.encode("latin-1")
            size = len(url)
        else:
            size = int(pathobj.get("size", 0))
        result = self.cache[path] = dict(
            st_uid=0, 
            st_gid=0, 
            st_mode=(S_IFDIR if is_dir else S_IFREG) | 0o444, 
            st_nlink=1, 
            st_size=size, 
            st_ctime=parse_as_ts(pathobj.get("created")), 
            st_mtime=parse_as_ts(pathobj.get("modified")), 
            st_atime=time(), 
            _as_strm=as_strm, 
        )
        if as_strm:
            result["_url"] = url
        return result

    def getattr(self, path: str, fh: int) -> dict:
        if basename(path).startswith("."):
            raise FuseOSError(ENOENT)
        try:
            return self.cache[path]
        except KeyError:
            pass
        fullpath = path
        as_strm = False
        if path.endswith(".strm") and self.strm_predicate and self.strm_predicate(path[:-5]):
            path = path[:-5]
            as_strm = True
        try:
            pathobj = self.fs.as_path(path, fetch_attr=True)
        except FileNotFoundError:
            logging.error(f"file not found: {path!r}")
            raise FuseOSError(ENOENT)
        else:
            return self._cache(pathobj, fullpath, as_strm=as_strm)

    def open(self, path: str, flags: int) -> int:
        try:
            if self.cache[path]["_as_strm"]:
                return 0
        except:
            logging.exception(f"can open file: {path!r}")
            return 0
        fh = self.next_fh()
        self.fh_to_file[fh] = self.fs.as_path(path).open("rb")
        return fh

    def read(self, path: str, size: int, offset: int, fh: int) -> bytes:
        if fh == 0:
            attr = self.cache[path]
            if attr["_as_strm"]:
                return attr["_url"][offset:offset+size]
        file = self.fh_to_file[fh]
        file.seek(offset)
        return file.read(size)

    @cached(TTLCache(64, ttl=10), key=lambda self, path, fh: path)
    def readdir(self, path: str, fh: int) -> list[str]:
        predicate = self.predicate
        strm_predicate = self.strm_predicate
        ls = [".", ".."]
        add = ls.append
        do_cache = self._cache
        for pathobj in self.fs.listdir_attr(path):
            is_dir = pathobj.is_dir()
            name = pathobj.name
            if name.startswith("."):
                continue
            subpath = joinpath(path, name)
            as_strm = False
            if not is_dir and strm_predicate and strm_predicate(name):
                name += ".strm"
                subpath += ".strm"
                as_strm = True
            elif predicate and not predicate(subpath + "/"[:is_dir]):
                continue
            do_cache(pathobj, subpath, as_strm=as_strm)
            add(name)
        return ls

    def release(self, path: str, fh: int):
        if fh:
            self.fh_to_file.pop(fh).close()


if __name__ == "__main__":
    log_level = args.log_level
    if isinstance(log_level, str):
        try:
            log_level = getattr(logging, log_level.upper(), None)
            if log_level:
                log_level = int(log_level)
            else:
                log_level = 999
        except:
            log_level = 999
    log_level = cast(int, log_level)
    logging.basicConfig(level=log_level)

    ls: list[str] = []
    strm_predicate = None
    if args.strm:
        ls.extend(read_str(args.strm))
    if args.strm_file:
        try:
            ls.extend(read_file(open(args.strm_file, encoding="utf-8")))
        except OSError:
            logging.exception(f"can't read file: {args.strm_file!r}")
    if ls:
        strm_predicate = parse(ls, check_mimetype=True)

    ls = []
    predicate = None
    if args.ignore:
        ls.extend(read_str(args.ignore))
    if args.ignore_file:
        try:
            ls.extend(read_file(open(args.ignore_file, encoding="utf-8")))
        except OSError:
            logging.exception(f"can't read file: {args.ignore_file!r}")
    if ls:
        ignore = parse(ls, check_mimetype=True)
        if ignore:
            predicate = lambda p: not ignore(p)

    print("\n    👋 Welcome to use alist fuse and strm 👏\n")
    # https://code.google.com/archive/p/macfuse/wikis/OPTIONS.wiki
    fuse = FUSE(
        AlistFuseOperations(
            args.origin, 
            args.username, 
            args.password, 
            cache=args.cache, 
            predicate=predicate, 
            strm_predicate=strm_predicate, 
        ),
        args.mount_point, 
        ro=True, 
        allow_other=args.allow_other, 
        foreground=not args.background, 
        nothreads=args.nothreads, 
        debug=args.debug, 
    )


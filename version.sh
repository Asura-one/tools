#!/bin/bash
# 自动更新版本号
# version: v0.1

revisioncount=`git log --oneline | wc -l`
projectversion=`git describe --tags --long`
cleanversion=${projectversion%%-*}

function VERSION() {
    select option in "alpha beta rc release"; do
        case $option in
            alpha )
                echo "\n内部测试版本"
                ;;
            beta )
                echo "\n公测版本"
                ;;
            rc )
                echo "\n正式版本的候选版本"
                ;;
            release )
                echo "\n正式版本"
                ;;
        esac
    done
    case $option in
        pattern )
            ;;
    esac
}

function TAG() {
    read -p "$(echo -e "\n请输入版本号：")" version
    git tag -a ${version} -m "Version ${version}"
}

function RELEASE() {
    echo -e "\n请选择先行版本"
    VERSION
    git describe --tags --always --dirty=${version}
}

echo "$projectversion-$revisioncount"
echo "$cleanversion.$revisioncount"

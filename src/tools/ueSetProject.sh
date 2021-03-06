nc="$(tput sgr0)"
bold="$(tput bold)"
blue="$(tput setaf 4)"
red="$(tput setaf 1)"
green="$(tput setaf 2)"
yellow="$(tput setaf 3)"

prj=$red
grp=$green
ast=$yellow

sp=`python $UE_PATH/src/tools/ueSetProject.py $*`

#function testComp
#{
#  COMPREPLY=()
#  local opt="testproj testgrp"
#  local cur=${COMP_WORDS[COMP_CWORD]}
#  COMPREPLY=($(compgen -W "$opt" -- $cur))
#}

#complete -F testComp uesp

if [[ $? == 1 ]]; then
  eval $sp

  if [[ -d $PROJ_ROOT/bin ]]; then
    export PATH=$PATH:$PROJ_ROOT/bin
  fi

  export PS1="[\[$prj\]$PROJ\[$nc\]:\[$grp\]$GRP\[$nc\]:\[$ast\]$ASST\[$nc\]]\n[\u@\h \W]\$ "

  cd $ASST_ROOT

  echo ""
  echo "${bold}Setting current asset to:$nc"
  echo "  Project: [ $prj$PROJ$nc ]"
  echo "  Group:   [ $grp$GRP$nc ]"
  echo "  Asset:   [ $ast$ASST$nc ]"
  echo ""
else
  echo -e $sp
fi


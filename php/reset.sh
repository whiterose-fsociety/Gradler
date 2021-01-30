#!/bin/bash

#Code To Communicate With php
SUCCESS_REQUEST_CODE=1
FAILED_REQUEST_CODE=0


#Functions
function reset(){
  gradle_arr=$1
  crawler=$2
  gradle_size=${#gradle_arr[@]}
  for ((i=0;i < $gradle_size;i++))
  do
    if [ -f $crawler/${gradle_arr[$i]} ]
    then
        rm $crawler/${gradle_arr[$i]}
        echo "File ${gradle_arr[$i]} Removed ..."
    fi
  done

  gradle_results=$3
  gradle_status=$4
  php=$5
  if [ -f $gradle_results -a $gradle_status ];
  then
    rm $gradle_results
    rm $gradle_status
    echo "File $gradle_results removed "
    echo "File $gradle_status removed "
  fi

}
# Constants
##Directories
crawler=../Crawler
gradle=gradle
tests=../Tests
php=php
##Variables
# package_name="$1"
package_name="com.example.attributechangeproject"
instrumented_name="ExampleInstrumentedTest.html"
unit_name="ExampleUnitTest.html"

# Files
gradle_results=gradle_results.json
gradle_status=gradle_status.txt
gradle_unit="gradle-$unit_name"
gradle_instrument="gradle-$instrumented_name"
gradle_arr=($gradle_results $gradle_unit $gradle_instrument)


reset $gradle_arr $crawler $gradle_results $gradle_status $php

<?php
require "conn.php";

define("ABS_DIR","/home/molefe/Software/Developer/AttributeChangeProject");
define("GRADLE_STATUS","gradle_status.txt");
define("GRADLE_FILE","gradle_results.json");
define("SUCCESS_REQUEST_CODE",1);

const timecreated = 1591649191;
const timemodified = 1592625291;
const grader = -1;
const attemptnumber = 1;

function getProjectName(){
  $explode = explode("/",ABS_DIR);
  $explode_size = count($explode);
  return $explode[$explode_size-1];
}
$project_name = getProjectName();



function cleanGradler(){
  $clean_output = shell_exec("./reset.sh");
//   echo "Cleaning Gradler ....<br>";
//   echo $clean_output."<br>";
}
function runGradler($project_name){
//   echo "Running Gradler...."."<br>";
  $output = shell_exec("./gradler.sh $project_name ".ABS_DIR);
}


function fetch_gradle_results($project_name){
  cleanGradler();
  runGradler($project_name);

  $gradle_file = fopen(GRADLE_STATUS,"r") or die("Unable To Open File");
  $value = fgets($gradle_file);
  fclose($gradle_file);

  $gradle_json = '{}';
  if(SUCCESS_REQUEST_CODE == $value){
    $gradle_json = file_get_contents(GRADLE_FILE);
  }else{
    shell_exec("./reset.sh");
    echo "Please Make Sure That Your Directory Is Correct";
  }

  return $gradle_json;
}


function insert_gradle_results($assignment,$userid,$grade){
    $sql = "INSERT INTO mdl_assign_grades (assignment,userid,timecreated,timemodified,grader,grade,attemptnumber) VALUES ('$assignment','$userid','timecreated','timemodified','grader','$grade','attemptnumber')";
    if ($conn->query($sql) == TRUE){
        echo "New Record Created Successfully";
    }else{
        echo "Error: ".$sql." <br>".$conn->error;
    }
}



$gradle_json = fetch_gradle_results($project_name);
$gradle_decode = json_decode($gradle_json,true)[0];
$gradle_unit_tests = $gradle_decode['unit'];
$gradle_instrumented_tests = $gradle_decode['instrumented'];
$gradle_status = $gradle_decode['status'];
$grade = explode("%",$gradle_status['grade'])[0];

// Assume these are the values
$assignment = 1;
$userid = 3;


if ($conn->connect_error){
    die("Connection Failed: ".$conn->connect_error);
}else{
    echo "Connected Successfully";
}

// insert_gradle_results($assignment,$userid,$grade);
 ?>

#!/bin/bash

ubuntu_version="$(lsb_release -r -s)"

if [ $ubuntu_version == "18.04" ]; then
  ROS_NAME="melodic"
#elif [ $ubuntu_version == "16.04" ]; then
#  ROS_NAME="kinetic"
#elif [ $ubuntu_version == "20.04" ]; then
#  ROS_NAME="noetic"
else
  echo -e "Unsupported Ubuntu version: $ubuntu_version"
  echo -e "This colab setup script only works with 18.04"
  exit 1
fi

if [ -d "/opt/ros/melodic" ]; then
  echo "ros-$ROS_NAME-desktop is already installed."
else
  start_time="$(date -u +%s)"

  echo "Ubuntu $ubuntu_version detected. ROS-$ROS_NAME chosen for installation.";

  echo -e "\e[1;33m ******************************************** \e[0m"
  echo -e "\e[1;33m The installation may take around 5  Minutes! \e[0m"
  echo -e "\e[1;33m ******************************************** \e[0m"
  sleep 4

  echo "deb http://packages.ros.org/ros/ubuntu bionic main" >> /etc/apt/sources.list.d/ros-latest.list
  echo "- deb added"

  apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654 >> /tmp/key.txt
  echo "- key added"

  apt update >> /tmp/update.txt
  echo "- apt updated"

  apt install ros-melodic-desktop  > /tmp/ros_install.txt
  echo "- ROS-$ROS_NAME-desktop installed.";

  end_time="$(date -u +%s)"
  elapsed="$(($end_time-$start_time))"

  echo "ROS installation complete, took $elapsed seconds in total"
fi
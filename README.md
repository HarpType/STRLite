# STRLite

## Installing STRLite
#### Installing ROS Kinetic Kame
1. Configure the Ubuntu repositories. There are four repositories in Ubuntu: Main, Universe, Restricted and Multiverse. To install ROS we should enable access to the entire repositories.
2. Set up your source.list. It adds the ROS repository informatino where the binaries are stored. Just execute the following commands in a terminal:

    `$ sudo sh -c 'echo "deb http://packages.ros. org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'`

3. Add the keys. The following is the command to add the keys:

`$ sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116`

4. Update the Ubuntu package list.

`$ sudo apt-get update`

5. Install ROS Kinetic packages.

`$ sudo apt-get install ros-kinetic-desktop-full`

6. Initialize rosdep. It is used for installing the dependent packages of a ROS package.

<code> $ sudo rosdep init </code>

<code> $ rosdep update </code>

7. Set the ROS environment. To access the ROS packages and command-line tools we have to set up the ROS environment. The following command adds a line in the .bashrc file (this file is in home folder), which sets the ROS environment in every new terminal.

<code> $ echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc </code>

The .bashrc file runs in every new terminal so the following command sets the environment in the current terminal:

<code> $ source ~/.bashrc </code>

8. Set up dependencies for building the package.

<code> $ sudo apt-get install python-rosinstall python-rosinstall-generator python-wstool build-essential </code>


#### Installing Rosbridge
1. Install rosbridge. The following command is used:

<code> $ sudo apt-get install ros-kinetic-rosbridge-server </code>

#### Seting up PostgreSQL
1. Install PostgreSQL.
2. Open the PostgreSQL console:

<code> $ sudo -u postgres psql postgres </code>

3. Create and set up a new user for the database.

`create user user_name with password 'password';`

`    alter role user_name set client_encoding to 'utf8';`

`   alter role user_name set timezone to 'UTC';`

`    alter role user_name createdb;`

4. Create database.

<code> create database django_db owner user_name; </code>

5. Set up django settings with your postgres.

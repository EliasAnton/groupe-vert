#!/usr/bin/env python3
import rospy

from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Point32
import std_msgs.msg

if __name__ == '__main__':
    '''
    Publishes example pointcloud
    '''
    rospy.init_node('point_polygon_scaler')
    pointcloud_publisher = rospy.Publisher("/my_pointcloud_topic", PointCloud)
    rospy.loginfo("pcl_publish_example")
    #giving some time for the publisher to register
    rospy.sleep(0.5)
    #declaring pointcloud
    my_awesome_pointcloud = PointCloud()
    #filling pointcloud header
    header = std_msgs.msg.Header()
    header.stamp = rospy.Time.now()
    header.frame_id = 'map'
    my_awesome_pointcloud.header = header
    #filling some points
    my_awesome_pointcloud.points.append(Point32(1.0, 1.0, 0.0))
    my_awesome_pointcloud.points.append(Point32(2.0, 2.0, 0.0))
    my_awesome_pointcloud.points.append(Point32(3.0, 3.0, 0.0))
    #publish
    pointcloud_publisher.publish(my_awesome_pointcloud)
    #exit. we are done!
    rospy.spin()
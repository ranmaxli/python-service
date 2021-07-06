/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50172
Source Host           : localhost:3306
Source Database       : petshop

Target Server Type    : MYSQL
Target Server Version : 50172
File Encoding         : 65001

Date: 2019-02-24 19:03:55
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for petshop_goodsbrief
-- ----------------------------
DROP TABLE IF EXISTS `petshop_goodsbrief`;
CREATE TABLE `petshop_goodsbrief` (
  `goods_herf` varchar(255) NOT NULL,
  `goods_name` varchar(255) DEFAULT NULL,
  `goods_price` varchar(255) DEFAULT NULL,
  `goods_salesValue` varchar(255) DEFAULT NULL,
  `goods_store` varchar(255) DEFAULT NULL,
  `send_address` varchar(255) DEFAULT NULL,
  `goods_url` varchar(255) DEFAULT NULL,
  `creat_date` varchar(255) DEFAULT NULL,
  `goods_key` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`goods_herf`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

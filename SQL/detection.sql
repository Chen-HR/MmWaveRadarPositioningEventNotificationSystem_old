-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2023-12-03 09:53:50
-- 伺服器版本： 10.4.24-MariaDB
-- PHP 版本： 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `positioning`
--

-- --------------------------------------------------------

--
-- 資料表結構 `detection`
--

CREATE TABLE `detection` (
  `Id` int(11) NOT NULL,
  `Ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Area` int(11) NOT NULL,
  `X_coordinate` float NOT NULL,
  `Y_coordinate` float NOT NULL,
  `Z_coordinate` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `detection`
--
ALTER TABLE `detection`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `Area` (`Area`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `detection`
--
ALTER TABLE `detection`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `detection`
--
ALTER TABLE `detection`
  ADD CONSTRAINT `Area` FOREIGN KEY (`Area`) REFERENCES `area` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

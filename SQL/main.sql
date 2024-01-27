
-- Data table structure `scenes`
CREATE TABLE `scenes` (
  `Id` int(11) NOT NULL,
  `Name` varchar(20) CHARACTER SET utf8 NOT NULL,
  `x_min` float NOT NULL, 
  `x_max` float NOT NULL, 
  `y_min` float NOT NULL, 
  `y_max` float NOT NULL,
  `TM_11` float NOT NULL, 
  `TM_12` float NOT NULL, 
  `TM_21` float NOT NULL, 
  `TM_22` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- Data table index `scenes`
ALTER TABLE `scenes`
  ADD PRIMARY KEY (`Id`);
-- Use table auto-increment (AUTO_INCREMENT) `scenes`
ALTER TABLE `scenes`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

-- Data table structure `area`
CREATE TABLE `area` (
  `Id` int(11) NOT NULL,
  `Scenes` int(11) NOT NULL,
  `Name` varchar(20) CHARACTER SET utf8 NOT NULL,
  `x_min` float NOT NULL, 
  `x_max` float NOT NULL, 
  `y_min` float NOT NULL, 
  `y_max` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- Data table index `area`
ALTER TABLE `area`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `Scenes` (`Scenes`);
-- Use table auto-increment (AUTO_INCREMENT) `area`
ALTER TABLE `area`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;
-- Data table restriction `area`
ALTER TABLE `area`
  ADD CONSTRAINT `Scenes` FOREIGN KEY (`Scenes`) REFERENCES `scenes` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

-- Data table structure `detection`
CREATE TABLE `detection` (
  `Id` int(11) NOT NULL,
  `Ts` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Area` int(11) NOT NULL,
  `x` float NOT NULL,
  `y` float NOT NULL,
  `z` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- Data table index `detection`
ALTER TABLE `detection`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `Area` (`Area`);
-- Use table auto-increment (AUTO_INCREMENT) `detection`
ALTER TABLE `detection`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;
-- Data table restriction `detection`
ALTER TABLE `detection`
  ADD CONSTRAINT `Area` FOREIGN KEY (`Area`) REFERENCES `area` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

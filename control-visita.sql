-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.0.30 - MySQL Community Server - GPL
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para control-visita
DROP DATABASE IF EXISTS `control-visita`;
CREATE DATABASE IF NOT EXISTS `control-visita` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `control-visita`;

-- Volcando estructura para tabla control-visita.users
DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla control-visita.users: ~2 rows (aproximadamente)
REPLACE INTO `users` (`id`, `username`, `password`, `email`, `created_at`) VALUES
	(1, 'admin2', 'scrypt:32768:8:1$S8FHSEKzQVpm7eQs$8f1c86c582ee0447a343f50d14627cf7d2c9e81816c216c87bac22c437da281789a71e6bcc7d4ec6eb8545aba5a10268310bf277a5078b9a9edd13d7d567a56a', 'llimi776@gmail.com', '2024-09-23 06:35:45'),
	(2, 'admin3', 'scrypt:32768:8:1$Vu5xP4eNNU7lgJ14$5ca3727364e89d9982b9cd099233389ba3160dddcf465e072a7fa09558d0626970a399f66fdc59cfcf9a53123fbc3c3a48d284591f0f2a8b0a07106e126e0fb8', 'llimi777@gmail.com', '2024-09-24 06:59:37');

-- Volcando estructura para tabla control-visita.visitantes
DROP TABLE IF EXISTS `visitantes`;
CREATE TABLE IF NOT EXISTS `visitantes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dni` varchar(8) DEFAULT NULL,
  `nombres` varchar(100) DEFAULT NULL,
  `apellido_paterno` varchar(100) DEFAULT NULL,
  `apellido_materno` varchar(100) DEFAULT NULL,
  `sexo` char(1) DEFAULT NULL,
  `edad` int DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `placa` varchar(10) DEFAULT NULL,
  `playa` varchar(100) DEFAULT NULL,
  `destino` varchar(100) DEFAULT NULL,
  `tipo_visita` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `dni` (`dni`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla control-visita.visitantes: ~2 rows (aproximadamente)
REPLACE INTO `visitantes` (`id`, `dni`, `nombres`, `apellido_paterno`, `apellido_materno`, `sexo`, `edad`, `direccion`, `placa`, `playa`, `destino`, `tipo_visita`) VALUES
	(1, '43169630', 'LLILMER', 'VISALOT', 'FERNANDEZ', 'M', 33, 'xxx', 'xxxxx', 'xxxx', 'xxxx', 'xxx'),
	(4, '42667652', 'LISSETH', 'CULQUIPOMA', 'HURTADO', 'M', 33, '333', 'xxxxx', 'xxxx', 'xxxx', 'visitante');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;

-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 18, 2025 at 07:50 AM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `keuangan`
--

-- --------------------------------------------------------

--
-- Table structure for table `budget`
--

CREATE TABLE `budget` (
  `id` int NOT NULL,
  `kategori` varchar(100) NOT NULL,
  `bulan` int NOT NULL,
  `tahun` int NOT NULL,
  `jumlah_budget` decimal(15,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `tipe_periode` varchar(20) DEFAULT 'bulanan',
  `minggu` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `budget`
--

INSERT INTO `budget` (`id`, `kategori`, `bulan`, `tahun`, `jumlah_budget`, `created_at`, `tipe_periode`, `minggu`) VALUES
(1, 'makan siang', 11, 2025, '35000.00', '2025-11-18 07:33:44', 'bulanan', NULL),
(2, 'jajan', 11, 2025, '10000.00', '2025-11-18 07:34:18', 'bulanan', NULL),
(3, 'bensin', 11, 2025, '50000.00', '2025-11-18 07:34:30', 'bulanan', NULL),
(4, 'Roti, air minum', 11, 2025, '10000.00', '2025-11-18 07:37:48', 'bulanan', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `setting`
--

CREATE TABLE `setting` (
  `id` int NOT NULL,
  `max_pengeluaran_weekly` decimal(10,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `transaksi`
--

CREATE TABLE `transaksi` (
  `id` int NOT NULL,
  `tanggal` date DEFAULT NULL,
  `jenis` text,
  `deskripsi` varchar(255) DEFAULT NULL,
  `jumlah` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `transaksi`
--

INSERT INTO `transaksi` (`id`, `tanggal`, `jenis`, `deskripsi`, `jumlah`) VALUES
(16, '2025-11-17', 'masuk', 'Jatah', 575000),
(17, '2025-11-17', 'keluar', 'bensin', 20000),
(19, '2025-11-17', 'keluar', 'makan siang', 13000),
(20, '2025-11-17', 'keluar', 'monthly fee', 9000),
(21, '2025-11-17', 'keluar', 'jajan', 2000),
(22, '2025-11-17', 'keluar', 'makan malam', 15000),
(24, '2025-11-18', 'keluar', 'Roti, air minum', 5000),
(27, '2025-11-18', 'keluar', 'Makan siang', 20000),
(28, '2025-11-18', 'keluar', 'Aoka', 2500),
(29, '2025-11-18', 'masuk', 'Sisa pecahan', 323);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int NOT NULL,
  `username` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL,
  `nama_lengkap` varchar(255) NOT NULL,
  `created_at` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password`, `nama_lengkap`, `created_at`) VALUES
(1, 'rakadit21', 'dityaka8@gmail.com', 'scrypt:32768:8:1$5D5AhTTLAD1yzcpN$22a4e9e5549180b109cfe8c61eb05a37d1dfc552d883bb500a8f119110d820d8f09dd441d4a9642082f2e587e4adaac5b45f65241e1c8c6d3d2614ca09d4b4c2', 'Raka Aditya', '2025-11-17 07:40:45.022858'),
(2, 'ling21', 'lingga@gmail.com', 'scrypt:32768:8:1$mfEWU1W2M8Nqxh2L$b2ebfc892ca8f15dccb0d5e5cc28e2aad4dbf7b23a3b6264697ee48f29742df8a7ac5c9ae80c25149a1bfc6a7f93630b4c1521af538b7df47d295c1f5da4e2d9', 'Lingga', '2025-11-17 07:44:59.882784');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `budget`
--
ALTER TABLE `budget`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_budget` (`kategori`,`bulan`,`tahun`,`tipe_periode`,`minggu`);

--
-- Indexes for table `setting`
--
ALTER TABLE `setting`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `transaksi`
--
ALTER TABLE `transaksi`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `budget`
--
ALTER TABLE `budget`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `setting`
--
ALTER TABLE `setting`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `transaksi`
--
ALTER TABLE `transaksi`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

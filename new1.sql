

CREATE TABLE user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_no VARCHAR(15),
    address TEXT
) ENGINE=InnoDB;
CREATE TABLE police_station (
    station_id INT AUTO_INCREMENT PRIMARY KEY,
    station_name VARCHAR(100) NOT NULL,
    address TEXT,
    city VARCHAR(50),
    district VARCHAR(50),
    state VARCHAR(50),
    contact_no VARCHAR(15)
) ENGINE=InnoDB;
CREATE TABLE officer (
    officer_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    rank VARCHAR(50),
    badge_no VARCHAR(20) UNIQUE,
    station_id INT,

    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (station_id) REFERENCES police_station(station_id)
) ENGINE=InnoDB;
CREATE TABLE complainant (
    complainant_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    age INT,
    gender VARCHAR(10),
    id_proof VARCHAR(50),

    FOREIGN KEY (user_id) REFERENCES user(user_id)
) ENGINE=InnoDB;
CREATE TABLE fir (
    fir_id INT AUTO_INCREMENT PRIMARY KEY,
    fir_no VARCHAR(20) UNIQUE,
    date_filed DATE,
    time_filed TIME,
    place_of_occurrence VARCHAR(200),
    description TEXT,
    status ENUM('Registered','Under Investigation','Pending Review','Rejected','Closed') 
           DEFAULT 'Registered',

    complainant_id INT,
    officer_id INT,
    station_id INT,

    FOREIGN KEY (complainant_id) REFERENCES complainant(complainant_id),
    FOREIGN KEY (officer_id) REFERENCES officer(officer_id),
    FOREIGN KEY (station_id) REFERENCES police_station(station_id)
) ENGINE=InnoDB;
CREATE TABLE investigation (
    investigation_id INT AUTO_INCREMENT PRIMARY KEY,
    fir_id INT,
    start_date DATE,
    end_date DATE,
    investigation_status VARCHAR(50),
    remarks TEXT,

    FOREIGN KEY (fir_id) REFERENCES fir(fir_id)
) ENGINE=InnoDB;
CREATE TABLE pass (
    officer_id INT,
    station_id INT,
    password VARCHAR(255),

    PRIMARY KEY (officer_id, station_id),

    FOREIGN KEY (officer_id) REFERENCES officer(officer_id),
    FOREIGN KEY (station_id) REFERENCES police_station(station_id)
) ENGINE=InnoDB;
USE fir_system;
INSERT INTO police_station (station_name, address, city, district, state, contact_no) VALUES
('Central Police Station','MG Road','Kochi','Ernakulam','Kerala','9876500001'),
('North Station','North Street','Kochi','Ernakulam','Kerala','9876500002'),
('South Station','South Avenue','Kochi','Ernakulam','Kerala','9876500003'),
('East Station','East End','Thrissur','Thrissur','Kerala','9876500004'),
('West Station','West Market','Calicut','Kozhikode','Kerala','9876500005'),
('Hill Station','Hill Road','Idukki','Idukki','Kerala','9876500006'),
('City Crime Branch','City Center','Kochi','Ernakulam','Kerala','9876500007'),
('Traffic Station','Main Junction','Kochi','Ernakulam','Kerala','9876500008'),
('Cyber Cell','Tech Park','Trivandrum','Trivandrum','Kerala','9876500009'),
('Rural Station','Village Road','Alappuzha','Alappuzha','Kerala','9876500010');

INSERT INTO user (name, contact_no, address) VALUES
('Rahul Sharma','9000000001','Kochi'),
('Anita Singh','9000000002','Kochi'),
('Vikram Das','9000000003','Thrissur'),
('Arjun Mehta','9000000004','Calicut'),
('Neha Patel','9000000005','Idukki'),
('Karan Verma','9000000006','Trivandrum'),
('Meera Nair','9000000007','Alappuzha'),
('Rohit Menon','9000000008','Kochi'),
('Sneha Pillai','9000000009','Thrissur'),
('Ajay Kumar','9000000010','Calicut');
INSERT INTO officer (user_id, rank, badge_no, station_id) VALUES
(1,'Inspector','INSP1001',1),
(2,'Sub Inspector','SI2002',1),
(3,'Head Constable','HC3003',2),
(4,'Inspector','INSP1004',3),
(5,'Sub Inspector','SI2005',4),
(6,'Inspector','INSP1006',5),
(7,'Sub Inspector','SI2007',6),
(8,'Head Constable','HC3008',7),
(9,'Inspector','INSP1009',8),
(10,'Sub Inspector','SI2010',9);
INSERT INTO complainant (user_id, age, gender, id_proof) VALUES
(1,34,'Male','Aadhaar'),
(2,29,'Female','PAN'),
(3,42,'Male','Voter ID'),
(4,31,'Male','Driving License'),
(5,27,'Female','Aadhaar'),
(6,38,'Male','PAN'),
(7,25,'Female','Aadhaar'),
(8,45,'Male','Passport'),
(9,30,'Female','Voter ID'),
(10,50,'Male','Driving License');
INSERT INTO fir 
(fir_no, date_filed, time_filed, place_of_occurrence, description, status, complainant_id, officer_id, station_id) 
VALUES
('FIR001','2026-03-01','10:00:00','MG Road','Theft complaint','Registered',1,1,1),
('FIR002','2026-03-02','11:00:00','North Street','Accident case','Under Investigation',2,2,1),
('FIR003','2026-03-03','12:00:00','South Avenue','Robbery','Pending Review',3,3,2),
('FIR004','2026-03-04','13:00:00','East End','Cyber fraud','Registered',4,4,3),
('FIR005','2026-03-05','14:00:00','West Market','Vehicle theft','Closed',5,5,4),
('FIR006','2026-03-06','15:00:00','Hill Road','Missing person','Registered',6,6,5),
('FIR007','2026-03-07','16:00:00','City Center','Assault case','Under Investigation',7,7,6),
('FIR008','2026-03-08','17:00:00','Main Junction','Traffic violation','Registered',8,8,7),
('FIR009','2026-03-09','18:00:00','Tech Park','Online scam','Pending Review',9,9,8),
('FIR010','2026-03-10','19:00:00','Village Road','Property dispute','Registered',10,10,9);

INSERT INTO investigation (fir_id, start_date, end_date, investigation_status, remarks) VALUES
(1,'2026-03-02',NULL,'Ongoing','Evidence collection'),
(2,'2026-03-03',NULL,'Ongoing','Witness statements'),
(3,'2026-03-04',NULL,'Pending','Under review'),
(4,'2026-03-05',NULL,'Ongoing','Cyber analysis'),
(5,'2026-03-06','2026-03-15','Completed','Case closed'),
(6,'2026-03-07',NULL,'Ongoing','Search operation'),
(7,'2026-03-08',NULL,'Ongoing','Medical report awaited'),
(8,'2026-03-09',NULL,'Ongoing','Traffic CCTV review'),
(9,'2026-03-10',NULL,'Pending','Bank details check'),
(10,'2026-03-11',NULL,'Ongoing','Legal consultation');

INSERT INTO pass (officer_id, station_id, password) VALUES
(1,1,'pass1'),
(2,1,'pass2'),
(3,2,'pass3'),
(4,3,'pass4'),
(5,4,'pass5'),
(6,5,'pass6'),
(7,6,'pass7'),
(8,7,'pass8'),
(9,8,'pass9'),
(10,9,'pass10');


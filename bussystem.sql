CREATE DATABASE Bus_system;
USE Bus_system;

CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    FullName VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    PhoneNumber VARCHAR(15),
    Role ENUM('Passenger', 'Admin') DEFAULT 'Passenger',
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE Buses (
    BusID INT AUTO_INCREMENT PRIMARY KEY,
    PlateNumber VARCHAR(50) UNIQUE NOT NULL,
    Capacity INT NOT NULL,
    BusType ENUM('Mini', 'Standard', 'Luxury') DEFAULT 'Standard'
);


CREATE TABLE Routes (
    RouteID INT AUTO_INCREMENT PRIMARY KEY,
    Source VARCHAR(100) NOT NULL,
    Destination VARCHAR(100) NOT NULL,
    DistanceKM INT NOT NULL
);


CREATE TABLE Schedules (
    ScheduleID INT AUTO_INCREMENT PRIMARY KEY,
    BusID INT NOT NULL,
    RouteID INT NOT NULL,
    DepartureTime DATETIME NOT NULL,
    ArrivalTime DATETIME NOT NULL,
    AvailableSeats INT NOT NULL,
    FOREIGN KEY (BusID) REFERENCES Buses(BusID) ON DELETE CASCADE,
    FOREIGN KEY (RouteID) REFERENCES Routes(RouteID) ON DELETE CASCADE
);


CREATE TABLE Tickets (
    TicketID INT AUTO_INCREMENT PRIMARY KEY,
    ScheduleID INT NOT NULL,
    UserID INT NOT NULL,
    SeatNumber INT NOT NULL,
    BookingDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ScheduleID) REFERENCES Schedules(ScheduleID) ON DELETE CASCADE,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

CREATE TABLE Feedbacks (
    FeedbackID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    BusID INT NOT NULL,
    Rating INT CHECK (Rating BETWEEN 1 AND 5),
    Comment TEXT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    FOREIGN KEY (BusID) REFERENCES Buses(BusID) ON DELETE CASCADE
);



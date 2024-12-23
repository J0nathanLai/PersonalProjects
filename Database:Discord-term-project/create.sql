-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2024-12-04 20:18:50.443

-- tables
-- Table: Administrators
CREATE TABLE Administrators (
    User_id int  NOT NULL,
    Identification_status boolean  NOT NULL,
    CONSTRAINT Administrators_pk PRIMARY KEY (User_id)
);

-- Table: Channel_messages
CREATE TABLE Channel_messages (
    Message_id int  NOT NULL,
    Chat_channel_id int  NOT NULL,
    CONSTRAINT Channel_messages_pk PRIMARY KEY (Message_id,Chat_channel_id)
);

-- Table: Chat_channels
CREATE TABLE Chat_channels (
    Chat_channel_id int  NOT NULL,
    Channel_name text  NOT NULL,
    Server_id int  NOT NULL,
    CONSTRAINT Chat_channels_pk PRIMARY KEY (Chat_channel_id)
);

-- Table: Community_members
CREATE TABLE Community_members (
    User_id int  NOT NULL,
    CONSTRAINT Community_members_pk PRIMARY KEY (User_id)
);

-- Table: Content_creators
CREATE TABLE Content_creators (
    User_id int  NOT NULL,
    Affiliate_link text  NOT NULL,
    Identification_status boolean  NOT NULL,
    CONSTRAINT Content_creators_pk PRIMARY KEY (User_id)
);

-- Table: Dm_messages
CREATE TABLE Dm_messages (
    Message_id int  NOT NULL,
    Receiver_id int  NOT NULL,
    CONSTRAINT Dm_messages_pk PRIMARY KEY (Message_id,Receiver_id)
);

-- Table: In_server
CREATE TABLE In_server (
    Server_id int  NOT NULL,
    User_id int  NOT NULL,
    Date_joined timestamp  NOT NULL,
    Can_chat boolean  NOT NULL,
    Can_voice boolean  NOT NULL,
    CONSTRAINT In_server_pk PRIMARY KEY (Server_id,User_id)
);

-- Table: In_voice_channel
CREATE TABLE In_voice_channel (
    User_id int  NOT NULL,
    Voice_channel_id int  NOT NULL,
    CONSTRAINT In_voice_channel_pk PRIMARY KEY (User_id)
);

-- Table: Messages
CREATE TABLE Messages (
    Message_id int  NOT NULL,
    Message text  NOT NULL,
    Time_sent timestamp  NOT NULL,
    Sender_id int  NOT NULL,
    CONSTRAINT Messages_pk PRIMARY KEY (Message_id)
);

-- Table: Reactions
CREATE TABLE Reactions (
    Reaction_id int  NOT NULL,
    Reaction_emoji text  NOT NULL,
    Time_added timestamp  NOT NULL,
    Message_id int  NOT NULL,
    User_id int  NOT NULL,
    CONSTRAINT Reactions_pk PRIMARY KEY (Reaction_id)
);

-- Table: Servers
CREATE TABLE Servers (
    Server_id int  NOT NULL,
    Date_created timestamp  NOT NULL,
    Server_name text  NOT NULL,
    Server_desc text  NOT NULL,
    CONSTRAINT Server_id PRIMARY KEY (Server_id)
);

-- Table: Users
CREATE TABLE Users (
    User_id int  NOT NULL,
    Username text  NOT NULL,
    Status status_type  NOT NULL,
    Status_message text  NOT NULL,
    Email text  NOT NULL,
    Age int  NOT NULL,
    Pronouns text  NOT NULL,
    CONSTRAINT Users_pk PRIMARY KEY (User_id)
);

-- Table: Voice_channels
CREATE TABLE Voice_channels (
    Voice_channel_id int  NOT NULL,
    Channel_name text  NOT NULL,
    Server_id int  NOT NULL,
    CONSTRAINT Voice_channels_pk PRIMARY KEY (Voice_channel_id)
);

-- foreign keys
-- Reference: Administrator_Users (table: Administrators)
ALTER TABLE Administrators ADD CONSTRAINT Administrator_Users
    FOREIGN KEY (User_id)
    REFERENCES Users (User_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Channel_messages_Chat_channels (table: Channel_messages)
ALTER TABLE Channel_messages ADD CONSTRAINT Channel_messages_Chat_channels
    FOREIGN KEY (Chat_channel_id)
    REFERENCES Chat_channels (Chat_channel_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Community_Member_Users (table: Community_members)
ALTER TABLE Community_members ADD CONSTRAINT Community_Member_Users
    FOREIGN KEY (User_id)
    REFERENCES Users (User_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Content_Creator_Users (table: Content_creators)
ALTER TABLE Content_creators ADD CONSTRAINT Content_Creator_Users
    FOREIGN KEY (User_id)
    REFERENCES Users (User_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Dm_messages_receiver (table: Dm_messages)
ALTER TABLE Dm_messages ADD CONSTRAINT Dm_messages_receiver
    FOREIGN KEY (Receiver_id)
    REFERENCES Users (User_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: In_voice_channel_Voice_channels (table: In_voice_channel)
ALTER TABLE In_voice_channel ADD CONSTRAINT In_voice_channel_Voice_channels
    FOREIGN KEY (Voice_channel_id)
    REFERENCES Voice_channels (Voice_channel_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Messages_Channel_messages (table: Channel_messages)
ALTER TABLE Channel_messages ADD CONSTRAINT Messages_Channel_messages
    FOREIGN KEY (Message_id)
    REFERENCES Messages (Message_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Messages_Dm_messages (table: Dm_messages)
ALTER TABLE Dm_messages ADD CONSTRAINT Messages_Dm_messages
    FOREIGN KEY (Message_id)
    REFERENCES Messages (Message_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Messages_Reactions (table: Reactions)
ALTER TABLE Reactions ADD CONSTRAINT Messages_Reactions
    FOREIGN KEY (Message_id)
    REFERENCES Messages (Message_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Messages_Users (table: Messages)
ALTER TABLE Messages ADD CONSTRAINT Messages_Users
    FOREIGN KEY (Sender_id)
    REFERENCES Users (User_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Servers_Chat_Channels (table: Chat_channels)
ALTER TABLE Chat_channels ADD CONSTRAINT Servers_Chat_Channels
    FOREIGN KEY (Server_id)
    REFERENCES Servers (Server_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Servers_Voice_Channels (table: Voice_channels)
ALTER TABLE Voice_channels ADD CONSTRAINT Servers_Voice_Channels
    FOREIGN KEY (Server_id)
    REFERENCES Servers (Server_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Users_In_voice_channel (table: In_voice_channel)
ALTER TABLE In_voice_channel ADD CONSTRAINT Users_In_voice_channel
    FOREIGN KEY (User_id)
    REFERENCES Users (User_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Users_Reactions (table: Reactions)
ALTER TABLE Reactions ADD CONSTRAINT Users_Reactions
    FOREIGN KEY (User_id)
    REFERENCES Users (User_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: is_in_Server (table: In_server)
ALTER TABLE In_server ADD CONSTRAINT is_in_Server
    FOREIGN KEY (Server_id)
    REFERENCES Servers (Server_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: is_in_User (table: In_server)
ALTER TABLE In_server ADD CONSTRAINT is_in_User
    FOREIGN KEY (User_id)
    REFERENCES Users (User_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.



-- -- Created by Vertabelo (http://vertabelo.com)
-- -- Last modification date: 2024-11-22 21:40:50.719

-- -- tables
-- -- Table: Servers
-- CREATE TABLE Servers (
--     Server_id int  NOT NULL,
--     Date_created timestamp  NOT NULL,
--     Server_name text  NOT NULL,
--     Server_desc text  NOT NULL,
--     CONSTRAINT Server_id PRIMARY KEY (Server_id)
-- );

-- -- Table: Users
-- CREATE TABLE Users (
--     User_id int  NOT NULL,
--     Username text  NOT NULL,
--     Status status_type  NOT NULL,
--     Status_message text  NOT NULL,
--     Email text  NOT NULL,
--     Age int  NOT NULL,
--     Pronouns text  NOT NULL,
--     CONSTRAINT Users_pk PRIMARY KEY (User_id)
-- );

-- -- Table: is_in
-- CREATE TABLE in_server (
--     Server_id int  NOT NULL,
--     User_id int  NOT NULL,
--     Date_joined timestamp  NOT NULL,
--     Can_chat boolean  NOT NULL,
--     Can_voice boolean  NOT NULL,
--     CONSTRAINT is_in_pk PRIMARY KEY (Server_id,User_id)
-- );

-- -- foreign keys
-- -- Reference: is_in_Server (table: is_in)
-- ALTER TABLE in_server ADD CONSTRAINT is_in_Server
--     FOREIGN KEY (Server_id)
--     REFERENCES Servers (Server_id)  
--     NOT DEFERRABLE 
--     INITIALLY IMMEDIATE
-- ;

-- -- Reference: is_in_User (table: is_in)
-- ALTER TABLE in_server ADD CONSTRAINT is_in_User
--     FOREIGN KEY (User_id)
--     REFERENCES Users (User_id)  
--     NOT DEFERRABLE 
--     INITIALLY IMMEDIATE
-- ;

-- -- End of file.


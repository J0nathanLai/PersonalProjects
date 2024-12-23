-- drop the trax database if it exists
DROP database if EXISTS discord;

-- create it afresh
CREATE database discord;
\c discord

CREATE TYPE status_type AS ENUM('offline', 'dnd', 'away', 'online', 'deleted');

\i create.SQL

-- load the data

\copy Servers(server_id, date_created, server_name, server_desc) FROM data/servers.csv csv header;
\copy Users(user_id, username, status, status_message, email, age, pronouns) FROM data/users.csv csv header;
\copy In_server(server_id, user_id, date_joined, can_chat, can_voice) FROM data/in_server.csv csv header;
\copy Administrators(user_id, identification_status) FROM data/administrators.csv csv header;
\copy Community_members(user_id) FROM data/community_members.csv csv header;
\copy Content_creators(user_id, affiliate_link, identification_status) FROM data/content_creators.csv csv header;
\copy Chat_channels(chat_channel_id, channel_name, server_id) FROM data/chat_channels.csv csv header;
\copy Voice_channels(voice_channel_id, channel_name, server_id) FROM data/voice_channels.csv csv header;
\copy Messages(message_id, message, time_sent, sender_id) FROM data/messages.csv csv header;
\copy Dm_messages(message_id, receiver_id) FROM data/dm_messages.csv csv header;
\copy Channel_messages(message_id, chat_channel_id) FROM data/channel_messages.csv csv header;
\copy In_voice_channel(user_id, voice_channel_id) FROM data/in_voice_channel.csv csv header;
\copy Reactions(reaction_id, reaction_emoji, time_added, message_id, user_id) FROM data/reactions.csv csv header;

-- \copy Features(fid, votes) FROM data/features.csv csv header;
-- \copy Comments(cid, date, iid, uid, comment) FROM data/comments.csv csv header;

CREATE OR REPLACE FUNCTION fn_deleted_user() 
RETURNS trigger 
LANGUAGE plpgsql AS 
$$
BEGIN
delete from in_server
where   user_id = old.user_id;

delete from in_voice_channel
where   user_id = old.user_id;
return NULL;
END
$$;

DROP TRIGGER IF EXISTS tr_deleted_user ON community_members; 

CREATE TRIGGER tr_deleted_user
AFTER DELETE ON community_members
FOR EACH ROW
  EXECUTE FUNCTION fn_deleted_user();

DROP TRIGGER IF EXISTS tr_deleted_user ON administrators; 

CREATE TRIGGER tr_deleted_user
AFTER DELETE ON administrators
FOR EACH ROW
  EXECUTE FUNCTION fn_deleted_user();

DROP TRIGGER IF EXISTS tr_deleted_user ON content_creators; 

CREATE TRIGGER tr_deleted_user
AFTER DELETE ON content_creators
FOR EACH ROW
  EXECUTE FUNCTION fn_deleted_user();
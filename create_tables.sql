CREATE TABLE channels (
    channelid SERIAL PRIMARY KEY,
    channelname VARCHAR(255) NOT NULL
);

CREATE TABLE videos (
    videoid SERIAL PRIMARY KEY,
    channelid INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    publishdate TIMESTAMP NOT NULL,
    FOREIGN KEY (channelid) REFERENCES channels(channelid)
);

CREATE TABLE comments (
    commentid SERIAL PRIMARY KEY,
    videoid INTEGER NOT NULL,
    author VARCHAR(255),
    commenttext TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    FOREIGN KEY (videoid) REFERENCES videos(videoid)
);

CREATE TABLE sentimentanalysis (
    analysisid SERIAL PRIMARY KEY,
    commentid INTEGER NOT NULL,
    sentimentscore NUMERIC NOT NULL,
    sentimentworded VARCHAR(255),
    analysistimestamp TIMESTAMP NOT NULL,
    FOREIGN KEY (commentid) REFERENCES comments(commentid)
);

CREATE TABLE iterations (
    iterationid SERIAL PRIMARY KEY,
    videoid INTEGER NOT NULL,
    fetchtimestamp TIMESTAMP NOT NULL,
    FOREIGN KEY (videoid) REFERENCES videos(videoid)
);


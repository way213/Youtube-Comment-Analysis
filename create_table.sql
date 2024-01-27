DROP TABLE IF EXISTS video_stats;
CREATE TABLE video_stats (
	videoId text NOT NULL PRIMARY KEY,
	videoTitle text NOT NULL,
	videoUploadDate TIMESTAMP NOT NULL,
	sentimentRetrivalDate TIMESTAMP NOT NULL,
	sentiment decimal(4,3) NOT NULL,
	topComment text NOT NULL
	);
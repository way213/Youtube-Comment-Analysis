# TEMPPPP
-- Insert or update a comment
INSERT INTO comments_table (comment_id, text, like_count, sentiment, ...)
VALUES ('new_comment_id', 'comment_text', new_like_count, 'sentiment_result', ...)
ON CONFLICT (comment_id)
DO
   UPDATE SET like_count = EXCLUDED.like_count,
              -- Add any other fields that might change and need to be updated
WHERE comments_table.like_count <> EXCLUDED.like_count;

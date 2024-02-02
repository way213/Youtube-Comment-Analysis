# create custom class to store comment details
class comment_details:
    def __init__(self, comment_id, text_display, text_original, like_count):
        self.comment_id = comment_id
        self.text_display = text_display
        self.text_original = text_original
        self.like_count = like_count
    def __getitem__(self, index):
        if index == 0:
            return self.comment_id
        elif index == 1:
            return self.text_display
        elif index == 2:
            return self.text_original
        elif index == 3:
            return self.like_count
        else:
            raise IndexError("Index out of range")
        
# our nodes
class CommentNode:
    def __init__(self, comment_id, text_display, text_original, like_count):
        self.comment_id = comment_id
        self.text_display = text_display
        self.text_original = text_original
        self.like_count = like_count + 1
        self.next = None

# linked list implementation
class CommentLinkedList:
    def __init__(self):
        self.head = None
        self.total_likes = 0;
        
    def add_comment(self, comment_node):
        self.total_likes = (self.total_likes + comment_node.like_count)
        if not self.head:
            self.head = comment_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = comment_node

    def display_comments(self):
        current = self.head
        while current:
            print(f'Comment: {current.text_original}, Likes: {current.like_count}')
            current = current.next


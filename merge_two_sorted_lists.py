# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        mergedList = cur = list1

        if  list1 == None:
            return list2

        if list2 == None:
            return list1

        if list1.val > list2.val:
            mergedList = cur = list2

        # list1 node compare with all elements in list2
        while list1 and list2:
            if list1.val <list2.val:
                cur.next = list1
                list1 = list1.next
            else:
                cur.next = list2
                list2 = list2.next
            cur = cur.next

        cur.next = list1 or list2

        return mergedList
        

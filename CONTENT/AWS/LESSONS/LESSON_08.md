# LESSON #8: Logic vulnerabilities
Logic vulnerabilities are usually a result of a poor or insecure design. 

## (8.1) Race Condition

A typical TOCTOU vulnerability, allowing an attacker to steal from the DVSA by submitting out-of-order requests.

In a normal scenario, the user will arrive at the billing stage on which payment details are sent to the application, only after the order was concluded by the user, and all other data was received.

However, re-submitting the "update" request right after the "billing" request, might end up with paying for less than what we managed to order.

Let's try. Assuming that we already completed all the relevant data. We have only (1) item in our cart that costs $25:

![alt cart](https://i.imgur.com/8H60Bym.png)

We will now send a *billing* request, and right after it an *update* request:

![alt billing](https://i.imgur.com/pNHnDM5.png)


![alt update](https://i.imgur.com/zuKCYDb.png)


As a result, we paid $25, as can be seen in the billing request. However, the receipt shows that we ordered 5 items, instead of one:

```

                Order: iEOXZ1jFEde8,
                
                To: 
                    Elisabeth Morty,
                    199 Square st., Oxford, UK
                
                Items:
                    Adidas DRI		25 (5)
		
                
                Total: $25

            	----------------------
		Date: 2018-12-18 14:56
```

- - -
[ToC](../LESSONS/README.md) | [1](../LESSONS/LESSON_01.md) | [2](../LESSONS/LESSON_02.md) | [3](../LESSONS/LESSON_03.md) | [4](../LESSONS/LESSON_04.md) | [5](../LESSONS/LESSON_05.md) | [6](../LESSONS/LESSON_06.md) | [7](../LESSONS/LESSON_07.md) | [8](../LESSONS/LESSON_08.md) | [9](../LESSONS/LESSON_09.md) | [10](../LESSONS/LESSON_10.md)

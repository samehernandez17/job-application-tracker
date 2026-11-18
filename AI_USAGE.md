# AI Usage Documentation
## Tools Used
- Claude for debugging, code review, and instructions
- Instinct for mapping out a daily plan of work and sending me reminders
## Key Prompts
1. "Could you map out a day to day plan based on the project specifications I uploaded. And please let me know how long toy think the project should take"
2. "Could you create any helper functions which would improve the readibility of my code in database.py"
3. "Could you create me a detailed instructions set for the the app.py so that I could follow, include examples of code"
4. "Could you explain the code you generated for app.py routes and how is using separate routes per action different to something like using only one function for both adding and editing"
5. "Could you check my app.py and database.py for any logic bugs"
6. "I have never worked with HTML or CSS so could you provide a brief explanation of how they work, provide an example page, and explain the code"
## What Worked Well
- The AI-generated databas.py helper functions helped improve my codes reliability, as every table reused them.
- The step by step instructions broke the app.py into manageable chunks and gave me a place to start the file
- Code explanations helped me understand how everything worked, especially the several ways to structure the routes, and how HTML and CSS worked 
- The debugging process was made effortless as the AI was able to find harder to detect logic errors in seconds, for example if errors: always being true because I called job_input twice
## What I Modified
- Added closing resources, as the AI didnt produce it, such as forgetting to close to the cursor 
-Fixed bugs which the AI generated code generated, such as poor syntax and producing wrong queries
- Renamed the helper functions so the code uses a uniform naming style and also organized the functions so that they were in a labeled section 
- Found that code generated did not match the project specifications so I had to modify it so it did so
- Kept the mysql password out of the code as to not hardcode it for only my pc 
## Lessons Learned
- I found that using AI was best for helping me get unstuck and also giving me a starting place at some instances. Asking AI for step-by-step instructions really helped break complicated or things I knew nothing about into manageable sections which I vould easily follow. Though I will say at some instances I had to turn to Stack Overflow as AI didnt get everything right and often I encountered errors in the code it generated. I found that asking AI for different ways of doing something very helpful as I got to see the tradeoffs associated with different methods. Eventhough I this time I took the simple repetitve way of doing things I felt like it was needed so that I could get a base understanding of how everything worked. Overall I think AI was a really good learning tool in this case and found it extremely helpful. 

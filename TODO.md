This should be a list of a bugs to fix or features to develop

### Bugs

- **Translate**: the yandex key is in, but KarmaBot crashes all the time due to an exception raised by the GET call. 
        Two measures:
            - fix the GET call (probably for the original dev as it lies within botbuiltins),
            - _[DONE 2016-03-02 15:17 ArtOfCode]_ confine the GET exception so that KarmaBot does not crash each time
        => _[DONE Update of Master]_
- **@KarmaBot cat**: with the new way to address KarmaBot, most of the commands are working. Some exceptions were noticed, like
            - cat
            - exec
            - detectlang
            - translate
        => _[DONE 2016-03-02 J_F_B_M]_
        Lost in the Master update. Should be added in the botbuiltins sudmodule again...
        

### Features

- Games: Some small interactive games to play with Karma and other users.
        - **Roulette** Bet points to get points
        - **Russian Roulette** Karma sends a message to which users can reply to participate. Once playercount is established, a "gun" is loaded and Karma asks one of the users to pull the trigger. Loser looses points?
- **Wise man says** Basically $>cat A wise man says *{{say}}*, but a wiser man says *{{say}}*
	=> Recovered.
- **Arithmetic** calculate sums, subtractions, multiplications, etc.
        - Maybe Regex it so it contains no letters and then execute it as code? Can Python do this? [J_F_B_M]
- **Work** each user can start a timer
        - can write as much as they want in the 5 minutes after the timer is started,
        - after the 5 minutes grace, the number of messages is accumulated
        - they get a warning if
                - they write more than 15 messages within a short time (tbd),
                - when the timer reaches 30 minutes, they have written at least 5 messages before the current one, and the last one was less 
                  than 10 minutes previously,
                - when they write at least 7 messages within one hour before the current one, and the last one was less than 15min before.
        - they get automatically removed from the list if they haven't written more than 5 messages in the last 60 minutes OR when they decide to stop the timer
        - it provides a status (diff work plugin status and work status) with current counts and when was the start
        => _[DONE BP 2016-03-07]_


### git

- Push current branches to remote repo:
                git push origin dev
                git checkout master
                git push origin master
                (back to dev: git checkout dev)







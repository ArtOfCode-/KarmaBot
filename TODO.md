This should be a list of a bugs to fix or features to develop

### Bugs

- **Translate**: the yandex key is in, but KarmaBot crashes all the time due to an exception raised by the GET call. 
        Two measures:
            - fix the GET call (probably for the original dev as it lies within botbuiltins),
            - _[DONE 2016-03-02 15:17 ArtOfCode]_ confine the GET exception so that KarmaBot does not crash each time
- **@KarmaBot cat**: with the new way to address KarmaBot, most of the commands are working. Some exceptions were noticed, like
            - cat
            - exec
        => _[DONE 2016-03-02 J_F_B_M]_
        

### Features

- Games: Some small interactive games to play with Karma and other users.
        - **Roulette** Bet points to get points
        - **Russian Roulette** Karma sends a message to which users can reply to participate. Once playercount is established, a "gun" is loaded and Karma asks one of the users to pull the trigger. Loser looses points?
- **Wise man says** Basically $>cat A wise man says *{{say}}*, but a wiser man says *{{say}}*
- **Arithmetic** calculate sums, subtractions, multiplications, etc.
        - Maybe Regex it so it contains no letters and then execute it as code? Can Python do this? [J_F_B_M]
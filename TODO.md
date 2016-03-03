This should be a list of a bugs to fix or features to develop

### Bugs

- **Translate**: the yandex key is in, but KarmaBot crashes all the time due to an exception raised by the GET call. 
        Two measures:
            - fix the GET call (probably for the original dev as it lies within botbuiltins),
            - [DONE 2016-03-02 15:17 ArtOfCode] confine the GET exception so that KarmaBot does not crash each time
- **@KarmaBot cat**: with the new way to address KarmaBot, most of the commands are working. Some exceptions were noticed, like
            - cat
            - exec
        => [DONE 2016-03-02 J_F_B_M]
        

### Features
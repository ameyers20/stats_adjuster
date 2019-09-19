# stats_adjuster
Most baseball fans choose to judge a player's skill based solely off their most basic statistics. Specifically, batting average, homerun total, and RBI total. The triple crown, a very coveted and rare honor is a feat accomplished by having the most of all three of these statistics. But the fallacy in this thinking is that not all ballparks are created equal. They all have unique dimensions and unique locations, and the impact of this on games is far from negligible. This application takes a look at the number of times a player played in each ballpark and adjusts their batting staistics accordingly. First, it calculates what the mean player would do with the input player's schedule. Then, it sees how many standard deviations from the mean input player was. Finally it finds the totals of those standard deviations from the mean of a standardized schedule (equal games at each ballpark). 

##Sample 

Alexs-MacBook-Pro-5:stats_adjuster alex$ python main.py
Enter a player name: Aaron Judge
Enter a team that they played for (3 letter acronym): NYA
Enter a season (1993-2018): 2017
Enter Aaron Judge's batting average in 2017: .284
Enter Aaron Judge's homerun total in 2017: 52
Enter Aaron Judge's RBI total in 2017: 114

With a standard schedule, Aaron Judge would have hit an estimated .285 with 46.5 homeruns  and 109.9 RBI's in 2017.

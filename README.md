# Computer Science Capstone 2023-2024

<h1>Project</h1>
AI that can read the instructions to a game and be able to play it

<h2>Notes</h2>

<h3>Article 1</h3>

[Atari AI Reads Instructions and Becomes 6000 Times Faster](https://singularityhub.com/2023/03/10/an-ai-learned-to-play-atari-6000-times-faster-by-reading-the-instructions/)

Carnegie Mellon researchers used a language model to extract key points in an Atari game instruction manual and used that information to ask questions to a LLM similar to GPT-3.  The answers to these questions were used to automatically create rewards and penalties for a reinforment-based learning AI, compared to just using the in-game score to create them.  This led to it learning 6000 times faster than other AIs; however, it does not perform as well as the leading model. Nonetheless, this technique can extend to any usage.
<h4>Method</h4>

1. Extract key points from instruction manual
1. Feed yes/no questions from key points to a LLM
1. Use questions and answers to create rewards and penalties
1. Use these rewards and penalties to train reinforment-learning algorithm

<h3>Article 2</h3>

[Google Deepmind AI Learns Rules of a Game As It's Playing](https://www.unite.ai/deepminds-new-ai-is-able-to-learn-the-rules-of-a-game-as-it-plays/)

Deepmind's AI is able to learn the rules of the game it is playing by narrowing down all of the important factors in the game, then analyzing what opponents do to make decisions and learn.  This approach is different than others in that it only takes in factors it thinks are relavent to the game and important to making moves instead of taking in every factor there is.
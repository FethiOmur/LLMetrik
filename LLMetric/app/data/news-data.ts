export interface NewsItem {
  title: string;
  description: string;
  summary: string;
  image: string;
  link: string;
}

export const newsItems: NewsItem[] = [
  {
    title: "GPT-5 Announcement",
    description:
      "OpenAI has officially announced GPT-5, promising unprecedented reasoning capabilities and multimodal understanding. The new model features a 10x larger parameter count than GPT-4, advanced reasoning capabilities, improved multimodal understanding, enhanced factual accuracy, reduced hallucinations, and an expanded context window of 100k tokens. This represents a significant leap forward in AI capabilities and is expected to set new benchmarks for performance across a wide range of tasks.",
    summary: 
      "OpenAI announced GPT-5 with 10x larger parameter count than GPT-4. Features improved reasoning, multimodal understanding, and reduced hallucinations. Context window expanded to 100k tokens.",
    image: "/news/gpt5.jpg",
    link: "/news/gpt-5-announcement"
  },
  {
    title: "Claude 3 Sonnet Released",
    description:
      "Anthropic has released Claude 3 Sonnet, a more efficient and cost-effective version of their flagship AI assistant. The new model is 2x faster than Claude 3 Opus while being 30% more cost-effective. It features improved coding capabilities, better instruction following, enhanced multilingual support, and new API features for developers. Sonnet represents a balanced approach between performance and efficiency in the Claude 3 family.",
    summary:
      "Anthropic released Claude 3 Sonnet, 2x faster than Opus and 30% more cost-effective. Offers better coding, instruction following and multilingual support.",
    image: "/news/claude3.jpg",
    link: "/news/claude-3-sonnet-released"
  },
  {
    title: "Llama 3 Open Source",
    description:
      "Meta has released Llama 3 as fully open source, allowing unrestricted commercial use and modification. This 70B parameter model is competitive with closed models while offering the flexibility of an open source license. The release has sparked a wave of community-driven improvements and implementations, accelerating innovation in the open source AI ecosystem and making powerful language models more accessible to developers worldwide.",
    summary:
      "Meta released Llama 3 as fully open source with unrestricted commercial use. The 70B parameter model is competitive with closed systems and sparks community innovation.",
    image: "/news/llama3.jpg",
    link: "/news/llama-3-open-source"
  },
  {
    title: "LLM Benchmark Results",
    description:
      "The latest MMLU and HELM benchmark results show significant improvements across all major language models. GPT-4 leads in reasoning tasks, Claude 3 tops in factuality, Llama 3 shows impressive gains, Mistral Large excels in coding, and Gemini Ultra improves in math. Overall, there's a 15% improvement across models compared to the previous generation, highlighting the rapid pace of advancement in LLM capabilities.",
    summary:
      "Latest benchmarks show major improvements across all LLMs. GPT-4 leads in reasoning, Claude 3 in factuality, and Mistral in coding. Overall 15% improvement from previous generation.",
    image: "/news/benchmark.jpg",
    link: "/news/llm-benchmark-results"
  },
  {
    title: "Mistral AI Raises $500M",
    description:
      "Mistral AI has secured $500 million in Series B funding, valuing the company at $5 billion. The French AI startup has gained significant attention for its efficient and powerful open models. With this funding, Mistral plans to expand its research team, enhance its computing infrastructure, and develop more specialized models for enterprise applications, positioning itself as a strong competitor in the rapidly evolving AI market.",
    summary:
      "Mistral AI secured $500M in Series B at a $5B valuation. Plans to expand research, enhance infrastructure, and develop specialized enterprise models.",
    image: "/news/mistral.jpg",
    link: "/news/mistral-ai-raises-500m"
  },
  {
    title: "New LLM Fine-tuning Technique",
    description:
      "Researchers have developed a new fine-tuning technique that reduces computational requirements by 80% while maintaining model performance. This breakthrough approach combines sparse activation patterns with targeted parameter updates, allowing for more efficient adaptation of large models to specific tasks. The technique promises to democratize fine-tuning by making it accessible to organizations with more limited computational resources.",
    summary:
      "New fine-tuning technique reduces computation by 80% while maintaining performance. Uses sparse activation with targeted updates to make fine-tuning accessible to more organizations.",
    image: "/news/finetuning.jpg",
    link: "/news/new-llm-fine-tuning-technique"
  },
] 
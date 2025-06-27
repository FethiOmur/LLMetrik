"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";
import { StarBorder } from "@/components/ui/star-border";
import { Send, ChevronRight } from "lucide-react";

function useDebounce<T>(value: T, delay: number = 500): T {
    const [debouncedValue, setDebouncedValue] = useState<T>(value);

    useEffect(() => {
        const timer = setTimeout(() => {
            setDebouncedValue(value);
        }, delay);

        return () => {
            clearTimeout(timer);
        };
    }, [value, delay]);

    return debouncedValue;
}

export type Action = {
    id: string;
    label: string;
    description?: string;
};

interface SearchResult {
    actions: Action[];
}

const allActions = [
    // OpenAI modelleri
    {
        id: "1",
        label: "GPT-4 Turbo",
        description: "OpenAI",
    },
    {
        id: "2",
        label: "GPT-4o",
        description: "OpenAI",
    },
    {
        id: "3",
        label: "GPT-4o mini",
        description: "OpenAI",
    },
    {
        id: "4",
        label: "GPT-4.1",
        description: "OpenAI",
    },
    {
        id: "5",
        label: "o1",
        description: "OpenAI",
    },
    {
        id: "6",
        label: "o3",
        description: "OpenAI",
    },
    {
        id: "7",
        label: "o4-mini",
        description: "OpenAI",
    },
    {
        id: "8",
        label: "GPT-3.5 Turbo",
        description: "OpenAI",
    },
    // Anthropic modelleri
    {
        id: "9",
        label: "Claude 3 Opus",
        description: "Anthropic",
    },
    {
        id: "10",
        label: "Claude 3.5 Sonnet",
        description: "Anthropic",
    },
    {
        id: "11",
        label: "Claude 3 Haiku",
        description: "Anthropic",
    },
    {
        id: "12",
        label: "Claude 3.7 Sonnet",
        description: "Anthropic",
    },
    {
        id: "13", 
        label: "Claude 2.1",
        description: "Anthropic",
    },
    // Google modelleri
    {
        id: "14",
        label: "Gemini 1.5 Pro",
        description: "Google",
    },
    {
        id: "15", 
        label: "Gemini 2.5 Pro",
        description: "Google",
    },
    {
        id: "16",
        label: "Gemini 2.0 Flash",
        description: "Google",
    },
    {
        id: "17",
        label: "Gemini 1.5 Flash",
        description: "Google",
    },
    {
        id: "18",
        label: "Gemma 3 27B",
        description: "Google",
    },
    {
        id: "19",
        label: "Gemma 3 4B",
        description: "Google",
    },
    // Meta modelleri
    {
        id: "20",
        label: "Llama 3 70B",
        description: "Meta",
    },
    {
        id: "21",
        label: "Llama 4 Scout",
        description: "Meta",
    },
    {
        id: "22",
        label: "Llama 3.1 70B",
        description: "Meta",
    },
    {
        id: "23",
        label: "Llama 3.2 90B",
        description: "Meta",
    },
    {
        id: "24",
        label: "Llama 3.3 70B",
        description: "Meta",
    },
    {
        id: "25",
        label: "Llama 3.2 1B",
        description: "Meta",
    },
    // Mistral modelleri
    {
        id: "26",
        label: "Mistral Large",
        description: "Mistral AI",
    },
    {
        id: "27",
        label: "Mixtral 8x7B",
        description: "Mistral AI",
    },
    {
        id: "28",
        label: "Mistral Medium",
        description: "Mistral AI",
    },
    {
        id: "29",
        label: "Mistral Small",
        description: "Mistral AI",
    },
    {
        id: "30",
        label: "Codestral",
        description: "Mistral AI",
    },
    // Diğer popüler modeller
    {
        id: "31", 
        label: "Grok 3 mini",
        description: "xAI",
    },
    {
        id: "32",
        label: "Grok 3",
        description: "xAI",
    },
    {
        id: "33",
        label: "DeepSeek R1",
        description: "DeepSeek",
    },
    {
        id: "34",
        label: "Command-R+",
        description: "Cohere",
    },
    {
        id: "35",
        label: "Qwen 2.5 72B",
        description: "Alibaba",
    },
    {
        id: "36",
        label: "Yi-Large",
        description: "01.AI",
    },
    {
        id: "37",
        label: "Jamba 1.6 Large",
        description: "AI21 Labs",
    },
    {
        id: "38",
        label: "Phi-4",
        description: "Microsoft",
    },
    {
        id: "39",
        label: "Sonar Large",
        description: "Perplexity",
    },
    {
        id: "40",
        label: "DBRX",
        description: "Databricks",
    },
    {
        id: "41",
        label: "Aya Expanse 32B",
        description: "Cohere",
    },
    {
        id: "42",
        label: "LFM 40B",
        description: "Liquid AI",
    },
    {
        id: "43",
        label: "Solar Pro",
        description: "Upstage",
    },
    {
        id: "44",
        label: "Nova Premier",
        description: "Amazon",
    },
    {
        id: "45",
        label: "Qwen3 32B",
        description: "Alibaba",
    },
    {
        id: "46",
        label: "Skylark Pro",
        description: "Bytedance",
    },
    {
        id: "47",
        label: "Reka Core",
        description: "Reka AI",
    },
    {
        id: "48",
        label: "MiniMax-Text-01",
        description: "MiniMax",
    },
    {
        id: "49", 
        label: "Baichuan 4",
        description: "Baichuan",
    },
    {
        id: "50",
        label: "OpenChat 3.5",
        description: "OpenChat",
    }
];

function ActionSearchBar({ actions = allActions }: { actions?: Action[] }) {
    const [query, setQuery] = useState("");
    const [result, setResult] = useState<SearchResult | null>(null);
    const [isFocused, setIsFocused] = useState(false);
    const [isTyping, setIsTyping] = useState(false);
    const [selectedAction, setSelectedAction] = useState<Action | null>(null);
    const debouncedQuery = useDebounce(query, 200);

    useEffect(() => {
        if (!isFocused) {
            setResult(null);
            return;
        }

        if (!debouncedQuery) {
            setResult({ actions: allActions });
            return;
        }

        const normalizedQuery = debouncedQuery.toLowerCase().trim();
        const filteredActions = allActions.filter((action) => {
            const searchableText = action.label.toLowerCase();
            return searchableText.includes(normalizedQuery);
        });

        setResult({ actions: filteredActions });
    }, [debouncedQuery, isFocused]);

    // Model seçildiğinde input içeriğini güncelle
    useEffect(() => {
        if (selectedAction) {
            setQuery(selectedAction.label);
            setIsFocused(false);
        }
    }, [selectedAction]);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        // Eğer seçili bir model varsa ve kullanıcı bir şeyler yazıyorsa,
        // seçili modeli temizleyip normal arama moduna geç
        if (selectedAction) {
            setSelectedAction(null);
            setQuery(e.target.value);
        } else {
            setQuery(e.target.value);
        }
        setIsTyping(true);
    };

    const container = {
        hidden: { opacity: 0, height: 0 },
        show: {
            opacity: 1,
            height: "auto",
            transition: {
                height: {
                    duration: 0.4,
                },
                staggerChildren: 0.1,
            },
        },
        exit: {
            opacity: 0,
            height: 0,
            transition: {
                height: {
                    duration: 0.3,
                },
                opacity: {
                    duration: 0.2,
                },
            },
        },
    };

    const item = {
        hidden: { opacity: 0, y: 20 },
        show: {
            opacity: 1,
            y: 0,
            transition: {
                duration: 0.3,
            },
        },
        exit: {
            opacity: 0,
            y: -10,
            transition: {
                duration: 0.2,
            },
        },
    };

    // Reset selectedAction when focusing the input
    const handleFocus = () => {
        // Input'a her tıklandığında dropdown'ı göster
        setIsFocused(true);
        
        // Eğer zaten bir model seçiliyse ve tekrar tıklanmışsa
        if (selectedAction) {
            // Tüm metni seç (bu seçili kalacak)
            setTimeout(() => {
                const input = document.activeElement as HTMLInputElement;
                if (input) {
                    input.select();
                }
            }, 0);
            
            // Model listesini açarken seçili modeli temizleme
            setSelectedAction(null);
            // Query'yi temizleme
            setQuery("");
        }
    };
    
    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (selectedAction) {
            console.log("Seçilen model:", selectedAction);
            // Burada seçilen modele göre yönlendirme veya işlem yapılabilir
            // Örneğin: router.push(`/models/${selectedAction.id}`);
        } else if (query.trim()) {
            console.log("Arama sorgusu:", query);
            // Burada arama sorgusuna göre işlem yapılabilir
            // Örneğin: router.push(`/search?q=${encodeURIComponent(query)}`);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        // Enter tuşuna basıldığında dropdown'ı kapat
        if (e.key === "Enter") {
            setIsFocused(false);
        }
    };

    return (
        <div className="w-full max-w-xl mx-auto">
            <div className="relative flex flex-col justify-start items-center">
                <StarBorder 
                    as="div" 
                    className="w-full"
                    color="white"
                >
                    <form
                        onSubmit={handleSubmit}
                        className="relative w-full"
                    >
                        <input
                            type="text"
                            placeholder="LLM model seçin veya arayın..."
                            value={selectedAction ? `${selectedAction.label} (${selectedAction.description})` : query}
                            onChange={handleInputChange}
                            onFocus={handleFocus}
                            onClick={handleFocus}
                            onKeyDown={handleKeyDown}
                            onBlur={() => {
                                // Odak kaybolduğunda dropdown'ı kapat ama gecikmeli olarak
                                // böylece kullanıcı model seçerken dropdown kaybolmaz
                                setTimeout(() => setIsFocused(false), 200)
                            }}
                            className={cn(
                                "w-full rounded-full bg-zinc-900/80 px-5 py-3 text-base text-white outline-none transition-all duration-300 placeholder:text-zinc-400 font-sans",
                                "backdrop-blur-sm border-none",
                                "focus:shadow-inner focus:shadow-white/5",
                                selectedAction ? "font-medium text-white shadow-[0_0_15px_rgba(255,255,255,0.1)]" : ""
                            )}
                        />
                        <button
                            type="submit"
                            className={cn(
                                "absolute right-2.5 top-1/2 -translate-y-1/2 rounded-full p-2 text-white transition-all duration-300",
                                selectedAction 
                                    ? "bg-gradient-to-r from-zinc-500 to-zinc-600 hover:from-zinc-400 hover:to-zinc-500 hover:shadow-[0_0_15px_rgba(255,255,255,0.2)]" 
                                    : "bg-gradient-to-r from-zinc-700 to-zinc-800 hover:from-zinc-600 hover:to-zinc-700 hover:shadow-[0_0_10px_rgba(255,255,255,0.15)]"
                            )}
                        >
                            <AnimatePresence mode="popLayout">
                                {selectedAction || query.length > 0 ? (
                                    <motion.div
                                        key="send"
                                        initial={{ y: -20, opacity: 0 }}
                                        animate={{ y: 0, opacity: 1 }}
                                        exit={{ y: 20, opacity: 0 }}
                                        transition={{ duration: 0.2 }}
                                    >
                                        <Send className="w-4 h-4" />
                                    </motion.div>
                                ) : (
                                    <motion.div
                                        key="search"
                                        initial={{ y: -20, opacity: 0 }}
                                        animate={{ y: 0, opacity: 1 }}
                                        exit={{ y: 20, opacity: 0 }}
                                        transition={{ duration: 0.2 }}
                                    >
                                        <ChevronRight className="w-4 h-4" />
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </button>
                    </form>
                </StarBorder>

                <div className="w-full">
                    <AnimatePresence>
                        {isFocused && result && !selectedAction && (
                            <motion.div
                                className="w-full border rounded-md shadow-sm overflow-hidden border-zinc-800 bg-zinc-900 mt-1 max-h-52 overflow-y-auto"
                                variants={container}
                                initial="hidden"
                                animate="show"
                                exit="exit"
                            >
                                <motion.ul className="divide-y divide-zinc-800/40">
                                    {result.actions.map((action) => (
                                        <motion.li
                                            key={action.id}
                                            className="px-4 py-2.5 flex items-center hover:bg-zinc-800 cursor-pointer font-sans group transition-colors"
                                            variants={item}
                                            layout
                                            onClick={() => setSelectedAction(action)}
                                        >
                                            <div className="flex items-center gap-2">
                                                <span className="text-sm font-medium text-gray-100 group-hover:text-white">
                                                    {action.label}
                                                </span>
                                                <span className="text-xs text-gray-400 group-hover:text-gray-300">
                                                    {action.description}
                                                </span>
                                            </div>
                                        </motion.li>
                                    ))}
                                </motion.ul>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            </div>
        </div>
    );
}

export { ActionSearchBar }; 
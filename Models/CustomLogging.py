import logging

from enum import Enum


class CustomLogging(Enum):
    TRACE = logging.INFO - 1
    INSIGHT = logging.INFO + 1
    VERBOSE = logging.INFO + 2
    DETAIL = logging.INFO + 3
    FINEST = logging.INFO + 4
    FINE = logging.INFO + 5
    EXTRA = logging.INFO + 6
    SHOWCASE = logging.INFO + 7
    DEEPDIVE = logging.INFO + 8
    PROFILER = logging.INFO + 9
    PERSISTENT = logging.INFO + 11
    ENDURANCE = logging.INFO + 12
    PROMINENT = logging.INFO + 13
    INQUISITIVE = logging.INFO + 14

    # TRACE: Detailed tracing information, often used for step-by-step debugging.
    # INSIGHT: Information providing valuable insights into the application's behavior.
    # VERBOSE: Highly detailed information, more than typical debugging messages.
    # DETAIL: Additional details that might be useful for troubleshooting.
    # FINEST: The finest level of detail, capturing extremely fine-grained information.
    # FINE: Fine-grained information, more detailed than the standard DEBUG level.
    # FINEST: Similar to FINE but capturing the most detailed information.
    # EXTRA: Extra information, providing additional context or details.
    # SHOWCASE: Highlighting noteworthy events or showcasing important occurrences.
    # DEEPDIVE: Deep and thorough information for in-depth analysis.
    # PROFILER: Logging information related to profiling and performance.
    # PERSISTENT: Information about persistent state or long-lasting events.
    # ENDURANCE: Information related to processes that endure over time.
    # PROMINENT: Significant and prominent events or milestones.
    # INQUISITIVE: Logging for inquisitive purposes, exploring and understanding behavior.

    @classmethod
    def add_custom_levels(cls):
        # logger = logging.getLogger('alive-progress')
        for level in cls:
            logging.addLevelName(level.value, level.name)

    @classmethod
    def add_tags_to_widget(cls, text_widget):
        # Define tag configurations for each logging and custom logging level with random colors
        tag_configs = {
            cls.get_name(logging.INFO): {"foreground": "#14eb1b"},  # Sample color: Green
            cls.get_name(logging.WARNING): {"foreground": "orange"},  # Sample color: Orange
            cls.get_name(logging.ERROR): {"foreground": "red"},  # Sample color: Red
            cls.get_name(logging.DEBUG): {"foreground": "#F7525F"},  # Sample color: Pink
            cls.get_name(logging.CRITICAL): {"foreground": "#f40b1e"},  # Sample color: Dark Red
            cls.INSIGHT.name: {"foreground": "#0F52BA"},  # Sample color: Royal Blue
            cls.VERBOSE.name: {"foreground": "#FFD700"},  # Sample color: Gold
            cls.DETAIL.name: {"foreground": "#8A2BE2"},  # Sample color: Blue Violet
            cls.FINEST.name: {"foreground": "#008080"},  # Sample color: Teal
            cls.FINE.name: {"foreground": "#228B22"},  # Sample color: Forest Green
            cls.EXTRA.name: {"foreground": "#B8860B"},  # Sample color: Dark Goldenrod
            cls.SHOWCASE.name: {"foreground": "#FF6347"},  # Sample color: Tomato
            cls.DEEPDIVE.name: {"foreground": "#4169E1"},  # Sample color: Royal Blue
            cls.PROFILER.name.lower(): {"foreground": "#800080"},  # Sample color: Purple
            cls.PERSISTENT.name: {"foreground": "#2E8B57"},  # Sample color: Sea Green
            cls.ENDURANCE.name: {"foreground": "#FF4500"},  # Sample color: Orange Red
            cls.PROMINENT.name: {"foreground": "#4B0082"},  # Sample color: Indigo
            cls.INQUISITIVE.name: {"foreground": "#9932CC"}  # Sample color: Dark Orchid
            # Add more tag configurations for custom logging levels if needed
        }

        # Apply tag configurations to the text widget
        for tag, config in tag_configs.items():
            text_widget.tag_config(tagName=tag, **config)

    @staticmethod
    def get_name(log_level):
        for name, value in vars(logging).items():
            if value == log_level:
                return name

import styles from './Tabs.module.css';

type TabItem = {
    label: string;
    value: string;
    count?: number;
};

type TabsProps = {
    tabs: TabItem[];
    value: string;
    onChange: (value: string) => void;
    className?: string;
};

export default function Tabs({ tabs, value, onChange, className }: TabsProps) {
    return (
        <div className={[styles.tabList, className ?? ''].filter(Boolean).join(' ')}>
            {tabs.map((tab) => {
                const isActive = tab.value === value;
                return (
                    <button
                        key={tab.value}
                        type="button"
                        className={[styles.tab, isActive ? styles.active : ''].filter(Boolean).join(' ')}
                        onClick={() => onChange(tab.value)}
                        aria-selected={isActive}
                        role="tab"
                    >
                        {tab.label}
                        {tab.count !== undefined && (
                            <span className={[styles.badge, isActive ? styles.badgeActive : ''].filter(Boolean).join(' ')}>
                                {tab.count}
                            </span>
                        )}
                    </button>
                );
            })}
        </div>
    );
}

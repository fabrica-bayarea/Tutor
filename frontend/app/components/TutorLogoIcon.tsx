type Props = {
    size?: number;
    strokeWidth?: number;
    color?: string;
    className?: string;
};

export default function TutorLogoIcon({ size = 22, strokeWidth = 1.8, color = '#f97316', className }: Props) {
    return (
        <svg
            width={size}
            height={size}
            viewBox="0 0 18 18"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className={className}
        >
            <path
                d="M8 0L0 0L0 14.4L8 18M8 0L8 18M8 0L10 0M8 18L10 18M10 0L18 0L18 14.4L10 18M10 0L10 18M2 4.8L6 4.8M2 8.4L6 8.4M12 4.8L16 4.8M12 8.4L16 8.4"
                fill="white"
                stroke={color}
                strokeWidth={strokeWidth}
                strokeLinecap="round"
                strokeLinejoin="round"
            />
        </svg>
    );
}

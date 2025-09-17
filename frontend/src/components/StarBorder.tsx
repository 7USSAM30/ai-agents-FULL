import React from 'react';

interface StarBorderProps {
  as?: React.ElementType;
  className?: string;
  color?: string;
  speed?: string;
  thickness?: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
  [key: string]: unknown;
}

const StarBorder = ({
  as: Component = 'button',
  className = '',
  color = '#06b6d4',
  speed = '4s',
  thickness = 3,
  children,
  ...rest
}: StarBorderProps) => {
  return (
    <Component
      className={`relative inline-block overflow-hidden rounded-[20px] ${className}`}
      style={{
        padding: `${thickness}px 0`,
        ...rest.style
      }}
      {...rest}
    >
      <div
        className="absolute w-[300%] h-[50%] opacity-20 bottom-[-10px] right-[-250%] rounded-full animate-star-movement-bottom z-0"
        style={{
          background: `radial-gradient(ellipse, ${color}, transparent 30%)`,
          animationDuration: speed
        }}
      ></div>
      <div
        className="absolute w-[300%] h-[50%] opacity-20 top-[-10px] left-[-250%] rounded-full animate-star-movement-top z-0"
        style={{
          background: `radial-gradient(ellipse, ${color}, transparent 30%)`,
          animationDuration: speed
        }}
      ></div>
      <div className="relative z-10 bg-gradient-to-b from-gray-900 to-black border border-cyan-500/30 text-white text-center text-[16px] py-[16px] px-[26px] rounded-[20px] shadow-lg">
        {children}
      </div>
    </Component>
  );
};

export default StarBorder;

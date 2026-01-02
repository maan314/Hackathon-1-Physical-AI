import React, { Suspense } from 'react';
import OriginalLayout from '@theme-original/Layout';

// Dynamically import the chatbot to avoid initial load issues
const RagChatbot = React.lazy(() => import('@site/src/components/RagChatbot'));

export default function Layout(props) {
  return (
    <>
      <OriginalLayout {...props} />
      <Suspense fallback={null}>
        <RagChatbot />
      </Suspense>
    </>
  );
}
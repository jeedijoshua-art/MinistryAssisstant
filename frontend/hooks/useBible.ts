import { useQuery } from '@tanstack/react-query';
import { BibleAPI } from '../lib/api';
import { BibleVerse } from '../types/api';

export function useBibleVerse(reference: string, translation: string = 'KJV') {
  return useQuery({
    queryKey: ['bible', reference, translation],
    queryFn: async () => {
      const data = await BibleAPI.getVerse(reference, translation);
      return data as BibleVerse[];
    },
    enabled: !!reference,
  });
}

export function useBibleSearch(query: string, translation: string = 'KJV') {
  return useQuery({
    queryKey: ['bible-search', query, translation],
    queryFn: async () => {
      const data = await BibleAPI.search(query, translation);
      return data;
    },
    enabled: !!query,
  });
}

export function useBibleTopic(topic: string) {
  return useQuery({
    queryKey: ['bible-topic', topic],
    queryFn: async () => {
      const data = await BibleAPI.getTopic(topic);
      return data;
    },
    enabled: !!topic,
  });
}

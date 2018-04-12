const config = {
  content: [
    {
      type: 'row',
      content: [
        {
          type: 'react-component',
          component: 'RealtimeChart',
          title: 'Decagon Realtime Chart',
          props: { chartName: 'Decagon-5TE', subscriptionPath: 'science/decagon' },
        },
        {
          type: 'react-component',
          component: 'ResizeAwareMap',
          title: 'Map',
        },
      ],
    },
  ],
};

export default config;

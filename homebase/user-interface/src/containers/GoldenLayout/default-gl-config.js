const config = {
  content: [
    {
      type: 'row',
      content: [
        {
          type: 'react-component',
          component: 'Camera',
          title: 'Camera #1',
          props: { cameraID: '1' },
        },
        // {
        //   type: 'react-component',
        //   component: 'RealtimeChart',
        //   title: 'Decagon Realtime Chart',
        //   props: { chartName: 'Decagon-5TE', eventName: 'science/decagon' },
        // },
        // {
        //   type: 'react-component',
        //   component: 'ResizeAwareMap',
        //   title: 'Map',
        // },
      ],
    },
  ],
};

export default config;

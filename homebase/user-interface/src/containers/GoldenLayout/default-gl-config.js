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
        {
          type: 'react-component',
          component: 'Counter',
          title: 'Counter Component',
        },
      ],
    },
  ],
};

export default config;

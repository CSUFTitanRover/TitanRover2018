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
          component: 'Chart',
          title: 'Chart',
        },
      ],
    },
  ],
};

export default config;
